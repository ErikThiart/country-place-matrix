#!/usr/bin/env python3
"""Build bounded, namespaced GeoNames reference candidates from pinned snapshots.

This is reference data, not country activation or a national postal directory.
Parents are either explicit GeoNames ADM edges or labelled same-source admin-code
joins. ISO identities continue to come from country-catalog.v1.json.
"""

from __future__ import annotations

import argparse
import collections
import gzip
import hashlib
import json
import math
import re
import shutil
import time
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "resources/data/geonames"
CACHE = ROOT / "var/reference-sources/geonames/2026-10-27"
HISTORICAL = {"PPLCH", "PPLH", "PPLQ", "PPLW", "PCLH", "PCLX"}
MAX_ARCHIVE_BYTES = 475_000_000
MAX_UNCOMPRESSED_BYTES = 3_000_000_000
MAX_LINE_BYTES = 65_536
MAX_FEATURE_ID = 100_000_000
MAX_SHARD_RECORDS = 100_000
MAX_SHARD_BYTES = 95 * 1024 * 1024
ZERO_CODES = {"", "00", "000", "0000"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def verified_sources(cache: Path, data: Path, fetch: bool = False) -> list[dict]:
    lock = read_json(data / "sources.json")
    for source in lock:
        path = cache / source["file"]
        if not path.is_file():
            if not fetch:
                raise ValueError(
                    f"Missing pinned snapshot {source['file']}; use --fetch or restore the retained snapshot"
                )
            if not source["url"].startswith("https://download.geonames.org/export/dump/"):
                raise ValueError("Unapproved snapshot host")
            cache.mkdir(parents=True, exist_ok=True)
            temporary = path.with_name(path.name + ".partial")
            count = 0
            started = time.monotonic()
            with urllib.request.urlopen(source["url"], timeout=60) as response, temporary.open("wb") as target:
                for block in iter(lambda: response.read(1024 * 1024), b""):
                    count += len(block)
                    if count > source["bytes"] or time.monotonic() - started > 900:
                        raise ValueError("Snapshot size/time bound exceeded")
                    target.write(block)
            if count != source["bytes"] or sha256(temporary) != source["sha256"]:
                temporary.unlink(missing_ok=True)
                raise ValueError(
                    "Upstream snapshot changed; review and pin a new revision instead of silently updating"
                )
            temporary.replace(path)
        if path.stat().st_size != source["bytes"] or sha256(path) != source["sha256"]:
            raise ValueError(f"Pinned snapshot checksum mismatch: {source['file']}")
    return lock


def zip_lines(path: Path, member: str):
    with zipfile.ZipFile(path) as archive:
        info = archive.getinfo(member)
        if info.file_size > MAX_UNCOMPRESSED_BYTES or info.compress_size > MAX_ARCHIVE_BYTES:
            raise ValueError("Archive resource bound exceeded")
        with archive.open(info) as stream:
            while line := stream.readline(MAX_LINE_BYTES + 1):
                if len(line) > MAX_LINE_BYTES:
                    raise ValueError("Source line exceeds declared bound")
                yield line.decode("utf-8", "strict").rstrip("\r\n")


def country_info(path: Path, countries: dict) -> tuple[dict, list[dict]]:
    result, excluded = {}, []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        row = line.split("\t")
        if len(row) < 18:
            raise ValueError("Malformed GeoNames country information row")
        code = row[0]
        record = {
            "source_country_code": code,
            "geoname_id": int(row[16]),
            "source_name": row[4],
            "languages": row[15].split(",") if row[15] else [],
        }
        if code not in countries:
            excluded.append(record)
            continue
        # GeoNames names, alpha-3 and numeric columns never overwrite canonical ISO data.
        result[code] = record
    return result, excluded


def source_rows(cache: Path):
    for line in zip_lines(cache / "allCountries.zip", "allCountries.txt"):
        row = line.split("\t")
        if len(row) != 19:
            raise ValueError("GeoNames extract must contain exactly nineteen fields")
        identity = int(row[0])
        if not 0 < identity <= MAX_FEATURE_ID:
            raise ValueError("GeoNames identity exceeds declared positive resource bound")
        yield row


def rank(feature: str) -> int:
    if feature in {"PCLI", "PCLD", "PCLF", "PCLS", "PCLIX"}:
        return 0
    match = re.fullmatch(r"ADM([1-5])", feature)
    return int(match[1]) if match else 6


def current(feature: str) -> bool:
    return feature not in HISTORICAL and not feature.endswith("H")


def kind(feature_class: str, feature: str, identity: int, root_id: int | None) -> str:
    if feature_class == "P":
        return "locality"
    if identity == root_id:
        return "country"
    match = re.fullmatch(r"ADM([1-5])", feature)
    return "admin" + match[1] if match else "admin_other"


def admin_key(country: str, codes: list[str], level: int) -> str | None:
    values = codes[:level]
    if len(values) != level or any(value in ZERO_CODES for value in values):
        return None
    return country + "." + ".".join(values)


def load_hierarchy(cache: Path) -> dict[int, list[int]]:
    result: dict[int, list[int]] = collections.defaultdict(list)
    for line in zip_lines(cache / "hierarchy.zip", "hierarchy.txt"):
        row = line.split("\t")
        if len(row) != 3:
            raise ValueError("Malformed GeoNames hierarchy row")
        if row[2] == "ADM":
            result[int(row[1])].append(int(row[0]))
    return dict(result)


def choose_parent(
    identity: int,
    country: str,
    feature: str,
    codes: list[str],
    root_id: int | None,
    admins: dict[int, tuple],
    admin_keys: dict[str, int],
    hierarchy: dict[int, list[int]],
) -> tuple[int | None, list[int], str, list[str]]:
    if identity == root_id:
        return None, [], "country_only", []
    child_rank = 7 if feature.startswith("PPL") or feature == "STLMT" else rank(feature)
    eligible = [
        parent
        for parent in hierarchy.get(identity, [])
        if parent != identity
        and parent in admins
        and admins[parent][0] == country
        and admins[parent][1] < child_rank
        and admins[parent][2]
    ]
    eligible = sorted(set(eligible))
    flags = []
    if len(eligible) > 8:
        flags.append("additional_source_parents_require_review")
    if eligible:
        maximum = max(admins[parent][1] for parent in eligible)
        most_specific = [parent for parent in eligible if admins[parent][1] == maximum]
        if len(most_specific) == 1:
            return most_specific[0], eligible[:8], "geonames_hierarchy", flags
        flags.append("multiple_same_level_source_parents")
    upper = min(4, child_rank - 1)
    for level in range(upper, 0, -1):
        key = admin_key(country, codes, level)
        parent = admin_keys.get(key) if key else None
        if parent and parent != identity:
            return parent, sorted({*eligible, parent})[:8], "derived_admin_codes", flags
    if root_id and root_id != identity:
        return (
            root_id,
            sorted({*eligible, root_id})[:8],
            "country_only",
            [*flags, "no_specific_administrative_parent"],
        )
    return None, eligible[:8], "unknown", [*flags, "no_resolved_country_or_administrative_parent"]


class Shards:
    def __init__(self, directory: Path):
        self.directory = directory
        self.opened: dict[str, tuple] = {}
        self.parts = collections.Counter()
        self.counts = collections.Counter()
        self.rows = collections.defaultdict(collections.Counter)
        self.files = []

    def append(self, country: str, record: dict) -> None:
        if country not in self.opened or self.counts[country] >= MAX_SHARD_RECORDS:
            self.close(country)
            self.parts[country] += 1
            path = self.directory / f"{country}-{self.parts[country]:03}.ndjson.gz"
            raw = path.open("wb")
            zipped = gzip.GzipFile(filename="", mode="wb", compresslevel=6, fileobj=raw, mtime=0)
            self.opened[country] = (path, raw, zipped)
            self.counts[country] = 0
            self.rows[country] = collections.Counter()
        path, raw, zipped = self.opened[country]
        zipped.write((json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8"))
        self.counts[country] += 1
        self.rows[country][record["feature_code"]] += 1

    def close(self, country: str) -> None:
        if country not in self.opened:
            return
        path, raw, zipped = self.opened.pop(country)
        zipped.close()
        raw.close()
        if path.stat().st_size > MAX_SHARD_BYTES:
            raise ValueError("Country shard exceeds repository/file processing bound")
        self.files.append(
            {
                "country_code": country,
                "path": "shards/" + path.name,
                "sha256": sha256(path),
                "bytes": path.stat().st_size,
                "records": self.counts[country],
                "feature_counts": dict(sorted(self.rows[country].items())),
            }
        )

    def finish(self) -> list[dict]:
        for country in list(self.opened):
            self.close(country)
        return sorted(self.files, key=lambda record: record["path"])


SPECIAL_NAMES = {
    "AC": ("SH", {"ascension", "ascension island"}),
    "TA": ("SH", {"tristan da cunha", "tristan da cunha island"}),
    "EA": ("ES", {"ceuta", "melilla"}),
    "IC": ("ES", {"canary islands", "comunidad autónoma de canarias", "canarias"}),
    "CQ": ("GG", {"sark", "island of sark"}),
    "DG": ("IO", {"diego garcia"}),
    "CP": ("FR", {"clipperton island", "clipperton", "île clipperton"}),
}


def selector_roots(candidates: list[dict]) -> tuple[list[dict], str, str | None]:
    """Keep the broadest named administrative roots, not duplicate sub-levels."""
    administrative = [item for item in candidates if re.fullmatch(r"ADM[1-5]", item["feature_code"])]
    if administrative:
        level = min(rank(item["feature_code"]) for item in administrative)
        return [item for item in administrative if rank(item["feature_code"]) == level], "administrative_roots", None
    gap = (
        "Reference feature is not a verified containment polygon or complete membership crosswalk"
        if candidates
        else "No source-backed special-context root found"
    )
    return candidates, "reference_root_only" if candidates else "missing_root", gap


def build(cache: Path, data: Path, catalog: dict, sources: list[dict], progress: bool = True) -> dict:
    countries = catalog["countries"]
    country_rows, excluded = country_info(cache / "countryInfo.txt", countries)
    hierarchy = load_hierarchy(cache)
    admins: dict[int, tuple] = {}
    admin_keys: dict[str, int] = {}
    ambiguous_admin_keys: set[str] = set()
    special: dict[str, list[dict]] = collections.defaultdict(list)
    source_counts = collections.Counter()
    excluded_codes = collections.Counter()
    selected = 0
    seen_ids = bytearray()
    for number, row in enumerate(source_rows(cache), 1):
        source_counts["total_features"] += 1
        identity = int(row[0])
        byte, bit = divmod(identity, 8)
        if byte >= len(seen_ids):
            seen_ids.extend(b"\0" * (byte + 1 - len(seen_ids)))
        if seen_ids[byte] & (1 << bit):
            raise ValueError(f"Duplicate source GeoNames identity {identity}")
        seen_ids[byte] |= 1 << bit
        source_country = row[8]
        canonical = source_country if source_country in countries else None
        if canonical is None:
            excluded_codes[source_country or "(unassigned)"] += 1
            continue
        feature_class, feature = row[6:8]
        identity = int(row[0])
        codes = row[10:14]
        if feature_class == "A":
            admins[identity] = (canonical, rank(feature), current(feature))
            match = re.fullmatch(r"ADM([1-4])", feature)
            if match and current(feature):
                key = admin_key(canonical, codes, int(match[1]))
                if key:
                    if key in admin_keys and admin_keys[key] != identity:
                        ambiguous_admin_keys.add(key)
                    admin_keys[key] = identity
        for selector, (country, names) in SPECIAL_NAMES.items():
            named = row[1].casefold() in names or row[2].casefold() in names
            is_root_feature = feature_class == "A" or feature in {"ISL", "ISLS", "ATOL", "PCLI", "PCLD"}
            if canonical == country and named and is_root_feature:
                special[selector].append(
                    {"geoname_id": identity, "name": row[1], "feature_code": feature, "admin_codes": codes}
                )
        if feature_class in {"A", "P"}:
            selected += 1
            source_counts[feature_class] += 1
        if progress and number % 2_000_000 == 0:
            print(json.dumps({"phase": "index", "source_rows": number, "selected": selected}), flush=True)
    for key in ambiguous_admin_keys:
        admin_keys.pop(key, None)

    output = data / "shards"
    staging = data / ".shards-building"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    writers = Shards(staging)
    coverage = {code: collections.Counter() for code in countries}
    parent_sources = collections.Counter()
    review_counts = collections.Counter()
    timezones = catalog["timezones"]
    root_ids = {code: row["geoname_id"] for code, row in country_rows.items()}
    special_ids = {item["geoname_id"] for items in special.values() for item in items}
    for number, row in enumerate(source_rows(cache), 1):
        canonical = row[8] if row[8] in countries else None
        if canonical is None:
            continue
        identity = int(row[0])
        feature_class, feature = row[6:8]
        if feature_class not in {"A", "P"} and identity not in special_ids:
            continue
        latitude, longitude = float(row[4]), float(row[5])
        if (
            not math.isfinite(latitude)
            or not math.isfinite(longitude)
            or not -90 <= latitude <= 90
            or not -180 <= longitude <= 180
        ):
            raise ValueError(f"Invalid source coordinate at GeoNames identity {identity}")
        codes = row[10:14]
        parent, parents, parent_source, flags = choose_parent(
            identity, canonical, feature, codes, root_ids.get(canonical), admins, admin_keys, hierarchy
        )
        names = list(dict.fromkeys(name for name in row[3].split(",") if name and name != row[1]))
        alternate_count = len(names)
        if alternate_count > 64:
            flags.append("additional_alternate_names_in_retained_source")
        if len(row[1]) > 200:
            flags.append("name_exceeds_current_database_bound")
        zone = row[17] or None
        if zone is None:
            flags.append("timezone_unknown")
        elif zone not in timezones:
            flags.append("timezone_not_in_pinned_iana_inventory")
        if not current(feature):
            flags.append("historical_or_abandoned_source_category")
        if row[9]:
            flags.append("additional_country_codes_require_review")
        record = {
            "kind": kind(feature_class, feature, identity, root_ids.get(canonical))
            if feature_class in {"A", "P"}
            else "territory_root",
            "geoname_id": identity,
            "source_key": f"geonames:{identity}",
            "country_code": canonical,
            "source_country_code": row[8],
            "feature_class": feature_class,
            "feature_code": feature,
            "name": row[1],
            "ascii_name": row[2],
            "alternate_names": names[:64],
            "alternate_name_count": alternate_count,
            "admin1_code": codes[0],
            "admin2_code": codes[1],
            "admin3_code": codes[2],
            "admin4_code": codes[3],
            "admin_code_key": admin_key(canonical, codes, rank(feature))
            if feature_class == "A" and rank(feature) <= 4
            else None,
            "latitude": latitude,
            "longitude": longitude,
            "timezone": zone,
            "canonical_timezone": timezones[zone]["canonical_name"] if zone in timezones else None,
            "population": int(row[14]),
            "modified_at": row[18],
            "browse_parent_geoname_id": parent,
            "parent_geoname_ids": parents,
            "parent_source": parent_source,
            "current_selectable": current(feature) and len(row[1]) <= 200,
            "review_flags": flags,
        }
        writers.append(canonical, record)
        coverage[canonical]["records"] += 1
        coverage[canonical]["current" if record["current_selectable"] else "historical_or_review"] += 1
        coverage[canonical][record["kind"]] += 1
        parent_sources[parent_source] += 1
        review_counts.update(flags)
        if progress and number % 2_000_000 == 0:
            print(
                json.dumps(
                    {
                        "phase": "write",
                        "source_rows": number,
                        "output_records": sum(c["records"] for c in coverage.values()),
                    }
                ),
                flush=True,
            )
    shards = writers.finish()
    if output.exists():
        shutil.rmtree(output)
    staging.replace(output)
    selectors = {}
    for selector, definition in catalog["selectors"].items():
        canonical = definition["country_code"]
        if selector in SPECIAL_NAMES:
            candidates = special.get(selector, [])
            roots, status, gap = selector_roots(candidates)
            selectors[selector] = {
                "country_code": canonical,
                "root_geoname_ids": sorted({item["geoname_id"] for item in roots}),
                "root_evidence": roots,
                "membership_status": status,
                "review_required": True,
                "gap": gap,
            }
        else:
            selectors[selector] = {
                "country_code": canonical,
                "root_geoname_ids": [root_ids[canonical]] if canonical in root_ids else [],
                "membership_status": "canonical_country_reference",
                "review_required": True,
                "gap": None if canonical in root_ids else "GeoNames country root unavailable",
            }
    manifest = {
        "schema_version": 1,
        "dataset_id": "geonames-2026-10-27",
        "license": "CC-BY-4.0",
        "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "attribution": "GeoNames, https://www.geonames.org/",
        "sources": sources,
        "shards": shards,
        "counts": dict(source_counts),
        "normalized_records": sum(item["records"] for item in shards),
        "compressed_shard_bytes": sum(item["bytes"] for item in shards),
        "coverage": {"countries": {code: dict(sorted(counts.items())) for code, counts in sorted(coverage.items())}},
        "country_roots": country_rows,
        "selectors": selectors,
        "parent_sources": dict(sorted(parent_sources.items())),
        "review_flag_counts": dict(sorted(review_counts.items())),
        "excluded_source_country_codes": dict(sorted(excluded_codes.items())),
        "excluded_country_info": excluded,
        "ambiguous_admin_keys": sorted(ambiguous_admin_keys),
        "semantics": {
            "place_namespace": "geonames:feature",
            "identity_validation": "all source identities positive, bounded and unique across the complete snapshot",
            "selectable": "source category and name-length eligibility only; never country approval, activation or verified address suitability",
            "population": "source population estimate; zero can mean unknown and is not evidence of an uninhabited place",
            "admin_code_namespace": "geonames:FIPS/admin (not ISO subdivision codes)",
            "parent_rule": "same-country explicit ADM hierarchy with decreasing source rank, otherwise labelled same-source admin-code join or country-only fallback",
            "names": "GeoNames primary and ASCII names plus up to64 untagged alternate names; no native-language or official-name claim",
            "ordering": "pinned source snapshot order; stable geonameId identities do not depend on order",
            "timezone": "source centroid candidate, not timezone boundary proof or an automatic branch default",
            "readiness": "reference candidates only; no country activation, current graph replacement or national postal completeness claim",
            "coverage_limit": "all available A/P features, including rural/zero-population places; GeoNames itself does not warrant exhaustive or current national coverage",
        },
    }
    write_json(data / "manifest.json", manifest)
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=CACHE)
    parser.add_argument("--output", type=Path, default=DATA)
    parser.add_argument("--catalog", type=Path, default=ROOT / "resources/data/country-catalog.v1.json")
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch only exact SHA-pinned missing snapshots; changed upstream data is rejected",
    )
    arguments = parser.parse_args()
    sources = verified_sources(arguments.cache, arguments.output, arguments.fetch)
    manifest = build(arguments.cache, arguments.output, read_json(arguments.catalog), sources)
    print(
        json.dumps(
            {
                "dataset_id": manifest["dataset_id"],
                "records": manifest["normalized_records"],
                "bytes": manifest["compressed_shard_bytes"],
                "shards": len(manifest["shards"]),
            }
        )
    )


if __name__ == "__main__":
    main()
