#!/usr/bin/env python3
"""Rebuild telephone reference data from the retained, licensed upstream snapshot.

This exports libphonenumber metadata; it does not implement a replacement phone
parser, infer a business's location from its number, or prove number assignment.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "resources/data/phone-metadata"
OUTPUT = ROOT / "resources/data/country-phone-reference.v1.json"
TYPES = (
    "fixedLine",
    "mobile",
    "tollFree",
    "premiumRate",
    "sharedCost",
    "personalNumber",
    "voip",
    "pager",
    "uan",
    "voicemail",
    "noInternationalDialling",
)
ATTRIBUTES = {
    "internationalPrefix": "international_prefix_pattern",
    "nationalPrefix": "national_prefix",
    "nationalPrefixForParsing": "national_prefix_for_parsing",
    "nationalPrefixTransformRule": "national_prefix_transform_rule",
    "preferredInternationalPrefix": "preferred_international_prefix",
    "preferredExtnPrefix": "preferred_extension_prefix",
    "leadingDigits": "leading_digits_pattern",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def lengths(value: str | None) -> list[int]:
    """Expand only the published metadata length grammar; preserve local-only separately."""
    if value is None:
        return []
    result: set[int] = set()
    for token in value.split(","):
        interval = re.fullmatch(r"\[(\d+)-(\d+)\]", token)
        if interval:
            start, end = map(int, interval.groups())
            require(1 <= start <= end <= 30, "Unbounded possible-number length range")
            result.update(range(start, end + 1))
        else:
            require(re.fullmatch(r"\d{1,2}", token) is not None, "Unknown possible-number length grammar")
            number = int(token)
            require(1 <= number <= 30, "Unsupported possible-number length")
            result.add(number)
    return sorted(result)


def pattern(node: ET.Element | None) -> str | None:
    if node is None:
        return None
    # Upstream patterns contain XML layout whitespace. Formatting templates are
    # deliberately handled separately so their meaningful spaces are retained.
    result = "".join("".join(node.itertext()).split())
    require(0 < len(result) <= 30000, "Missing or oversized numbering pattern")
    re.compile(result)
    return result


def region_record(territory: ET.Element) -> dict:
    region, code = territory.get("id"), territory.get("countryCode")
    require(region == "001" or re.fullmatch(r"[A-Z]{2}", region or "") is not None, "Invalid source region")
    require(re.fullmatch(r"[1-9]\d{0,2}", code or "") is not None, "Invalid source calling code")
    general = pattern(territory.find("generalDesc/nationalNumberPattern"))
    require(general is not None, "Region has no general numbering pattern")
    descriptions = {}
    for kind in TYPES:
        node = territory.find(kind)
        if node is None:
            continue
        possible = node.find("possibleLengths")
        example = node.findtext("exampleNumber")
        if example is not None:
            example = example.strip()
            require(re.fullmatch(r"[0-9]{1,30}", example) is not None, "Invalid illustrative number")
        number_pattern = pattern(node.find("nationalNumberPattern"))
        national = lengths(possible.get("national") if possible is not None else None)
        local = lengths(possible.get("localOnly") if possible is not None else None)
        if example is not None:
            require(
                re.fullmatch(number_pattern or general, example) is not None,
                f"Source example mismatch: {region}/{kind}",
            )
            require(re.fullmatch(general, example) is not None, f"General example mismatch: {region}/{kind}")
            require(not national or len(example) in national, f"Source example length mismatch: {region}/{kind}")
        descriptions[kind] = {
            "national_number_pattern": number_pattern,
            "possible_national_lengths": national,
            "possible_local_only_lengths": local,
            "example_national_number": example,
        }
    formats = [
        {
            "pattern": node.get("pattern"),
            "leading_digits_patterns": [pattern(n) for n in node.findall("leadingDigits")],
            "format": node.findtext("format"),
            "international_format": node.findtext("intlFormat"),
            "national_prefix_formatting_rule": node.get("nationalPrefixFormattingRule"),
            "national_prefix_optional_when_formatting": node.get("nationalPrefixOptionalWhenFormatting") == "true",
            "carrier_code_formatting_rule": node.get("carrierCodeFormattingRule"),
        }
        for node in territory.findall("availableFormats/numberFormat")
    ]
    return {
        "region_code": region,
        "country_calling_code": code,
        "main_country_for_calling_code": territory.get("mainCountryForCode") == "true",
        "mobile_number_portable_region": territory.get("mobileNumberPortableRegion") == "true",
        **{target: territory.get(source) for source, target in ATTRIBUTES.items()},
        "general_national_number_pattern": general,
        "number_types": descriptions,
        "available_formats": formats,
    }


def build(metadata: bytes, catalog: dict, source: dict, catalog_sha: str) -> dict:
    require(source.get("license") == "Apache-2.0", "Source license must be explicit")
    territories = ET.fromstring(metadata).findall("territories/territory")
    require(100 <= len(territories) <= 1000, "Unexpected metadata region inventory")
    regions, non_geographic = {}, {}
    for node in territories:
        record = region_record(node)
        region, code = record["region_code"], record["country_calling_code"]
        destination, key = (non_geographic, code) if region == "001" else (regions, region)
        require(key not in destination, "Duplicate source numbering identity")
        destination[key] = record
    require(not ({"AN", "CS", "UK", "XA", "XB"} & regions.keys()), "Retired/pseudo regions cannot become current plans")
    require(set(regions) <= set(catalog["selectors"]), "New upstream region needs explicit country-catalog review")
    selectors = {}
    for code, selector in sorted(catalog["selectors"].items()):
        canonical = selector["country_code"]
        require(canonical in catalog["countries"], "Selector references an unknown canonical country")
        direct = regions.get(code)
        selectors[code] = {
            "canonical_country_code": canonical,
            "metadata_region": code if direct else None,
            "country_calling_code": direct["country_calling_code"] if direct else None,
            "status": "direct_upstream_region" if direct else "no_direct_region_metadata",
            "canonical_region_reference": canonical if canonical in regions else None,
            # A geography alias is not evidence that a numbering plan applies to
            # the island/context. Never turn canonical identity into a silent hint.
            "canonical_numbering_fallback_applied": False,
        }
    groups: dict[str, dict] = {}
    for region, record in sorted(regions.items()):
        group = groups.setdefault(record["country_calling_code"], {"regions": [], "main_region": None})
        group["regions"].append(region)
        if record["main_country_for_calling_code"]:
            require(group["main_region"] is None, "Calling code has multiple main regions")
            group["main_region"] = region
    for group in groups.values():
        if len(group["regions"]) == 1:
            group["main_region"] = group["regions"][0]
        require(group["main_region"] in group["regions"], "Shared calling code lacks an explicit main region")
    require(not (groups.keys() & non_geographic.keys()), "Geographic and non-geographic calling plans overlap")
    aliases = {
        code: {
            "action": a["action"],
            "canonical_country_code": a["country_code"],
            "replacement_selectors": a["replacement_selectors"],
        }
        for code, a in sorted(catalog["aliases"].items())
    }
    return {
        "schema_version": 1,
        "version": "libphonenumber-" + source["release"] + "-v1",
        "source": {k: source[k] for k in ("repository", "release", "published_at", "commit", "license", "files")},
        "country_catalog": {"version": catalog["version"], "sha256": catalog_sha},
        "usage": {
            "reference_only": True,
            "parser_implemented": False,
            "number_assignment_or_reachability_verified": False,
            "examples_are_upstream_illustrations_not_contact_destinations": True,
            "business_contacts_may_have_a_different_numbering_region_from_their_address": True,
            "non_geographic_001_is_not_a_listing_country": True,
        },
        "regions": dict(sorted(regions.items())),
        "non_geographic_calling_codes": dict(sorted(non_geographic.items(), key=lambda item: int(item[0]))),
        "calling_code_groups": dict(sorted(groups.items(), key=lambda item: int(item[0]))),
        "selectors": selectors,
        "aliases": aliases,
        "coverage": {
            "geographic_regions": len(regions),
            "non_geographic_plans": len(non_geographic),
            "selectors": len(selectors),
            "selectors_without_direct_metadata": [c for c, r in selectors.items() if r["metadata_region"] is None],
            "canonical_countries_without_direct_metadata": sorted(set(catalog["countries"]) - set(regions)),
        },
    }


def verified_sources(snapshot: Path, fetch: bool = False) -> tuple[bytes, dict]:
    manifest = json.loads((snapshot / "manifest.json").read_text())
    require(manifest.get("schema_version") == 1, "Unsupported source manifest schema")
    require(
        manifest.get("repository") == "https://github.com/google/libphonenumber", "Source repository must be explicit"
    )
    require(manifest.get("license") == "Apache-2.0", "Source license must be explicit")
    require(re.fullmatch(r"[a-f0-9]{40}", manifest.get("commit", "")) is not None, "Source commit must be immutable")
    require(re.fullmatch(r"v\d+\.\d+\.\d+", manifest.get("release", "")) is not None, "Source release must be explicit")
    files = manifest.get("files")
    require(isinstance(files, list) and 2 <= len(files) <= 3, "Source inventory must retain metadata and license")
    names = [entry.get("path") for entry in files if isinstance(entry, dict)]
    require(all(isinstance(name, str) for name in names), "Source filenames must be strings")
    require(
        len(names) == len(files) == len(set(names)) and {"PhoneNumberMetadata.xml", "LICENSE"} <= set(names),
        "Source inventory must retain unique metadata and license files",
    )
    allowed = {"PhoneNumberMetadata.xml": "resources/PhoneNumberMetadata.xml", "LICENSE": "LICENSE", "NOTICE": "NOTICE"}
    for entry in manifest["files"]:
        require(entry["path"] in allowed, "Unknown source filename")
        filename = snapshot / entry["path"]
        require(
            filename.parent == snapshot and not filename.is_symlink(),
            "Source filename must be a real direct snapshot child",
        )
        require(
            isinstance(entry.get("bytes"), int) and 0 < entry["bytes"] <= 5 * 1024 * 1024,
            "Source byte count must be bounded",
        )
        require(re.fullmatch(r"[a-f0-9]{64}", entry.get("sha256", "")) is not None, "Source checksum must be explicit")
        expected_url = (
            f"https://raw.githubusercontent.com/google/libphonenumber/{manifest['commit']}/{allowed[entry['path']]}"
        )
        require(
            entry.get("url") == expected_url and entry.get("upstream_path") == allowed[entry["path"]],
            "Source URL must match the official pinned file",
        )
        if fetch:
            with urllib.request.urlopen(entry["url"], timeout=30) as response:
                payload = response.read(5 * 1024 * 1024 + 1)
            require(
                len(payload) == entry["bytes"] and hashlib.sha256(payload).hexdigest() == entry["sha256"],
                "Downloaded source differs from the reviewed snapshot",
            )
            filename.write_bytes(payload)
        payload = filename.read_bytes()
        require(
            len(payload) == entry["bytes"] and hashlib.sha256(payload).hexdigest() == entry["sha256"],
            "Retained source checksum mismatch",
        )
    return (snapshot / "PhoneNumberMetadata.xml").read_bytes(), manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fetch-sources", action="store_true", help="Re-fetch exact pinned files; never adopt latest implicitly"
    )
    parser.add_argument("--check", action="store_true", help="Verify that the committed derived JSON is current")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    metadata, manifest = verified_sources(SNAPSHOT, args.fetch_sources)
    catalog_bytes = (ROOT / "resources/data/country-catalog.v1.json").read_bytes()
    result = build(metadata, json.loads(catalog_bytes), manifest, hashlib.sha256(catalog_bytes).hexdigest())
    encoded = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        require(args.output.read_text() == encoded, "Country phone reference needs rebuilding")
    else:
        args.output.write_text(encoded)
    print(json.dumps({"version": result["version"], **result["coverage"]}, sort_keys=True))


if __name__ == "__main__":
    main()
