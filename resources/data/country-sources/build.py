#!/usr/bin/env python3
"""Build the reviewed country identity snapshot offline. Never imports address/provider rules."""

import argparse
import hashlib
import json
import re
import tarfile
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE = Path(__file__).resolve().parent
OUTPUT = SOURCE.parent / "country-catalog.v1.json"
SPECIAL = {"AC": "SH", "CP": "FR", "CQ": "GG", "DG": "IO", "EA": "ES", "IC": "ES", "TA": "SH"}
TZ_FILES = [
    "africa",
    "antarctica",
    "asia",
    "australasia",
    "europe",
    "northamerica",
    "southamerica",
    "etcetera",
    "factory",
    "backward",
]


def expand_regions(text):
    result = set()
    for token in text.split():
        if "~" in token:
            first, ending = token.split("~")
            if len(first) != 2 or len(ending) != 1:
                raise ValueError("Unexpected CLDR region range")
            result.update(first[:-1] + chr(code) for code in range(ord(first[-1]), ord(ending) + 1))
        else:
            result.add(token)
    return result


def build():
    manifest = json.loads((SOURCE / "manifest.v1.json").read_text())
    for record in manifest["files"]:
        if Path(record["file"]).name != record["file"]:
            raise ValueError("Source file must be local and explicitly named")
        data = (SOURCE / record["file"]).read_bytes()
        if len(data) != record["bytes"] or hashlib.sha256(data).hexdigest() != record["sha256"]:
            raise ValueError("Pinned source checksum mismatch: " + record["file"])
    names = json.loads((SOURCE / "cldr-territories-en-49.json").read_text())["main"]["en"]["localeDisplayNames"][
        "territories"
    ]
    region = ET.parse(SOURCE / "cldr-region-49.xml").find(".//id[@type='region'][@idStatus='regular']")
    regular = expand_regions(region.text)
    codes = {
        row.get("type"): row.attrib
        for row in ET.parse(SOURCE / "cldr-supplemental-49.xml").findall(".//territoryCodes")
    }
    aliases = ET.parse(SOURCE / "cldr-metadata-49.xml").findall(".//territoryAlias")
    with tarfile.open(SOURCE / "tzdata-2026e.tar.gz") as archive:

        def text(name):
            # Named members only: no archive extraction or executable code is evaluated.
            return archive.extractfile(name).read().decode("utf-8")

        if text("version").strip() != manifest["tzdb_version"]:
            raise ValueError("IANA version mismatch")
        iso = dict(
            line.split("\t", 1) for line in text("iso3166.tab").splitlines() if line and not line.startswith("#")
        )
        zones, links = set(), {}
        for name in TZ_FILES:
            for line in text(name).splitlines():
                fields = line.split("#", 1)[0].split()
                if len(fields) >= 2 and fields[0] == "Zone":
                    zones.add(fields[1])
                if len(fields) >= 3 and fields[0] == "Link":
                    links[fields[2]] = fields[1]
        all_zones = zones | set(links)
        inventory = []
        for kind in ["zone.tab", "zone1970.tab"]:
            for line in text(kind).splitlines():
                if not line or line.startswith("#"):
                    continue
                fields = line.split("\t")
                if len(fields) < 3 or fields[2] not in all_zones:
                    raise ValueError("Unknown IANA country timezone")
                # zone1970 can name several countries sharing post1970 clock history.
                for country in fields[0].split(","):
                    if country not in iso:
                        raise ValueError("Unknown country in IANA timezone table")
                    inventory.append({"country_code": country, "timezone": fields[2], "kind": kind})
    if len(iso) != 249 or regular != set(iso) | set(SPECIAL) | {"XK"}:
        raise ValueError("Country/selector membership changed; an explicit catalog review is required")
    countries = {}
    for code in sorted(set(iso) | {"XK"}):
        assigned = code in iso
        crosswalk = codes.get(code, {})
        alpha3, numeric = crosswalk.get("alpha3"), crosswalk.get("numeric")
        if assigned and (not re.fullmatch("[A-Z]{3}", alpha3 or "") or not re.fullmatch("[0-9]{3}", numeric or "")):
            raise ValueError("Missing ISO code crosswalk for " + code)
        display = names[code]
        alternate = sorted(
            set(
                [value for key, value in names.items() if key.startswith(code + "-alt-")]
                + ([iso[code]] if assigned else [])
            )
            - {display}
        )
        countries[code] = {
            "code": code,
            "name": display,
            "status": "iso_assigned" if assigned else "exceptional",
            "iso_alpha3": alpha3 if assigned else None,
            "iso_numeric": numeric if assigned else None,
            "name_aliases": alternate,
        }
    selectors = {}
    for code in sorted(regular):
        canonical = SPECIAL.get(code, code)
        selectors[code] = {
            "code": code,
            "label": names[code],
            "country_code": canonical,
            "territory_code": code if code in SPECIAL and code != "EA" else None,
            "requires_place_choice": code == "EA",
            "status": "cldr_selector" if code in SPECIAL else countries[code]["status"],
        }
    history = {}
    for alias in aliases:
        code = alias.get("type")
        if not re.fullmatch("[A-Z]{2}", code) or code in selectors:
            continue
        replacements = alias.get("replacement", "").split()
        history[code] = {
            "code": code,
            "action": "normalise" if code == "UK" else "choose" if len(replacements) > 1 else "retired",
            "country_code": "GB" if code == "UK" else None,
            "replacement_selectors": [value for value in replacements if value in selectors],
            "source_replacements": replacements,
            "reason": alias.get("reason"),
        }

    def target(name):
        seen = set()
        while name in links:
            if name in seen:
                raise ValueError("IANA alias cycle")
            seen.add(name)
            name = links[name]
        if name not in zones:
            raise ValueError("Unknown canonical IANA zone")
        return name

    timezones = {
        name: {"name": name, "canonical_name": target(name), "kind": "link" if name in links else "zone"}
        for name in sorted(all_zones)
    }
    return {
        "version": manifest["catalog_version"],
        "cldr_version": manifest["cldr_version"],
        "tzdb_version": manifest["tzdb_version"],
        "countries": countries,
        "selectors": selectors,
        "timezones": timezones,
        "timezone_inventory": sorted(inventory, key=lambda row: (row["country_code"], row["timezone"], row["kind"])),
        "aliases": dict(sorted(history.items())),
        "sources": manifest,
        "limits": {
            "national_rules": "not_supplied",
            "phone_rules": "not_supplied",
            "timezone_inventory_is_context_approval": False,
            "iso_basis": manifest["iso_assignment_basis"],
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    output = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if (
            OUTPUT.read_text() != output
            or OUTPUT.with_suffix(".sha256").read_text().strip() != hashlib.sha256(output.encode()).hexdigest()
        ):
            raise SystemExit("Country catalog differs from its pinned sources")
        print("Pinned country catalog matches all reviewed sources.")
    else:
        OUTPUT.write_text(output)
        OUTPUT.with_suffix(".sha256").write_text(hashlib.sha256(output.encode()).hexdigest() + "\n")
        print("Built country identity metadata only; no national readiness or database changes.")
