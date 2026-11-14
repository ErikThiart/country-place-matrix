#!/usr/bin/env python3
"""Render reference-data evidence for every supported selector, without activation.

Uses retained versioned catalogs only. This report distinguishes canonical-country
counts from exceptional-selector membership and never substitutes parent phone or
timezone values for missing direct metadata.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUTS = {
    "catalog": "resources/data/country-catalog.v1.json",
    "address": "resources/data/country-address-metadata.v1.json",
    "full_address": "resources/data/country-addresses.v1.json",
    "geonames": "resources/data/geonames/manifest.json",
    "phone": "resources/data/country-phone-reference.v1.json",
    "postal_evidence": "resources/data/addressing/postal-evidence.v1.json",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_inputs(root: Path = ROOT) -> tuple[dict, dict]:
    inputs, hashes = {}, {}
    for key, relative in INPUTS.items():
        content = (root / relative).read_bytes()
        inputs[key] = json.loads(content)
        hashes[key] = hashlib.sha256(content).hexdigest()
    require(inputs["address"]["country_catalog_sha256"] == hashes["catalog"], "Address catalog fingerprint mismatch")
    require(inputs["phone"]["country_catalog"]["sha256"] == hashes["catalog"], "Phone catalog fingerprint mismatch")
    require(
        inputs["address"]["full_bundle_sha256"] == hashes["full_address"], "Full address bundle fingerprint mismatch"
    )
    return inputs, hashes


def build_rows(inputs: dict) -> list[dict]:
    catalog, addresses, full, geo, phones = (
        inputs[key] for key in ["catalog", "address", "full_address", "geonames", "phone"]
    )
    countries, selectors = catalog["countries"], catalog["selectors"]
    require(len(countries) == 250 and len(selectors) == 257, "Unexpected canonical/selector inventory")
    require(
        sum(country["status"] == "iso_assigned" for country in countries.values()) == 249,
        "Expected 249 ISO identities and explicit non-ISO XK",
    )
    require(countries["XK"]["status"] == "exceptional", "XK must remain explicitly non-ISO")
    for source in [addresses, full, geo, phones]:
        require(set(source["selectors"]) == set(selectors), "Selector source inventory mismatch")
    require(set(geo["coverage"]["countries"]) == set(countries), "GeoNames canonical inventory mismatch")
    subdivision_counts = collections.Counter(row["country_code"] for row in full["subdivisions"])
    zones = collections.defaultdict(collections.Counter)
    for zone in catalog["timezone_inventory"]:
        zones[zone["country_code"]][zone["kind"]] += 1
    rows = []
    for selector, identity in sorted(selectors.items()):
        canonical = identity["country_code"]
        address = addresses["selectors"][selector]
        address = address.get("address_reference", address)
        location, phone = geo["selectors"][selector], phones["selectors"][selector]
        require(address["country_code"] == canonical, f"Address canonical mismatch: {selector}")
        require(location["country_code"] == canonical, f"GeoNames canonical mismatch: {selector}")
        require(phone["canonical_country_code"] == canonical, f"Phone canonical mismatch: {selector}")
        require(not phone["canonical_numbering_fallback_applied"], "Parent phone fallback must remain disabled")
        require(address["format_status"] in ["dedicated", "parent", "generic"], "Unknown format provenance")
        counts = geo["coverage"]["countries"][canonical]
        administrative = sum(value for key, value in counts.items() if key == "country" or key.startswith("admin"))
        pattern = address.get("postal_code_pattern")
        pattern_state = (
            ("pattern-ok" if address.get("postal_pattern_compiles") is True else "pattern-invalid")
            if pattern
            else ("source-unused" if address["postal_code_status"] == "not_used" else "unknown")
        )
        rows.append(
            {
                "selector": selector,
                "label": identity["label"],
                "canonical": canonical,
                "canonical_name": countries[canonical]["name"],
                "identity_status": identity["status"],
                "requires_place_choice": identity["requires_place_choice"],
                "format": address["format_status"],
                "format_country": address["format_country_code"],
                "pattern": pattern_state,
                "valid_source_examples": len(address.get("postal_code_examples_valid", [])),
                "official_examples": len(address.get("official_postal_code_examples", [])),
                "source_conflicts": len(address.get("source_example_conflicts", [])),
                "optional_capture_overlay": any(
                    row["kind"] == "optional_postcode_capture" for row in address.get("overlays", [])
                ),
                "postal_subdivisions": subdivision_counts[canonical],
                "geo_administrative": administrative,
                "geo_localities": counts.get("locality", 0),
                "geo_historical_or_review": counts.get("historical_or_review", 0),
                "membership": location["membership_status"],
                "membership_gap": location.get("gap"),
                "membership_roots": location["root_geoname_ids"],
                "phone_region": phone["metadata_region"],
                "calling_code": phone["country_calling_code"],
                "zone_tab": zones[selector]["zone.tab"],
                "zone1970": zones[selector]["zone1970.tab"],
                "public_activation_approved": address["public_activation_approved"],
            }
        )
    return rows


def cell(value) -> str:
    return str(value).replace("|", "&#124;").replace("\n", " ")


def render(inputs: dict, hashes: dict) -> str:
    rows = build_rows(inputs)
    formats = collections.Counter(row["format"] for row in rows)
    direct_phone = sum(row["phone_region"] is not None for row in rows)
    no_zone = [row["selector"] for row in rows if not row["zone_tab"] and not row["zone1970"]]
    conflicts = [row["selector"] for row in rows if row["source_conflicts"]]
    geo, addresses, phones = (inputs[key] for key in ["geonames", "address", "phone"])
    lines = [
        "# Country data evidence matrix",
        "",
        "<!-- Generated by bin/build-country-readiness.py. Update source evidence, then rebuild; do not hand-edit rows. -->",
        "",
        (
            "The retained real-source inventory covers **257 selectors / 250 canonical identities (249 ISO plus explicit non-ISO XK)**. "
            "These rows record usable reference data and exact remaining gaps. They do not approve publication or national/provider/legal acceptance. "
            "See [country policy and code invariants](mapping-contract.md) for the activation boundary."
        ),
        "",
        (
            f"Address formats: **{formats['dedicated']} dedicated, {formats['parent']} explicitly inherited, {formats['generic']} generic**. "
            f"Postal subdivision references: **{len(inputs['full_address']['subdivisions']):,}**. "
            f"GeoNames: **{geo['normalized_records']:,}** retained features across every canonical country. "
            f"Direct telephone regions: **{direct_phone}/257**; missing values remain unknown."
        ),
        "",
        (
            f"Strict-source example conflicts remain visible for **{', '.join(conflicts)}**. Separately attributed postal examples exist for "
            f"**{', '.join(addresses['coverage']['countries_with_official_examples'])}**; they do not rewrite upstream conflicts or submitted postcodes. "
            "Somalia’s dated spacing evidence is unresolved and supplies no current display hint."
        ),
        "",
        (
            f"No direct IANA country-table association exists for **{', '.join(no_zone)}**. Source feature timezone candidates remain separate; "
            "neither UTC nor a parent-country timezone/phone plan is substituted."
        ),
        "",
        "## Reading the rows",
        "",
        "- **Format** gives dedicated/parent/generic provenance and the source format country. Parent formats require territory applicability review; generic layouts do not prove postal fields are unused.",
        "- **Postal** gives strict source pattern status, then `valid upstream + separately attributed examples / upstream conflicts`. `source-unused` describes that pinned format, not national absence. `capture` marks the reviewed optional field overlay without inventing a strict pattern.",
        "- **Postal nodes** and **Geo A/P** count the entire canonical country: postal subdivision records, administrative features / populated features. Exceptional selectors must not inherit those counts as territory membership. Historical/abandoned categories and overlong names remain in counts with `current_selectable=false`; other review flags are separate.",
        "- **Membership** distinguishes canonical roots, source administrative roots and reference-only points/features. `choice` requires separate Ceuta/Melilla selection. All imported graph candidates still require review; counts are not exhaustive street/rural coverage.",
        "- **Phone** shows direct region/calling-code metadata only. **TZ** gives direct `zone.tab / zone1970.tab` associations, not a reviewed branch timezone or boundary. Neither proves assignment, reachability, geocoder support or business location.",
        "",
        "| Selector / display name | Canonical | Format | Postal: valid + attributed / conflicts | Postal nodes | Geo A / P (canonical) | Membership | Phone | TZ |",
        "| --- | --- | --- | --- | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        postal = (
            f"{row['pattern']}: {row['valid_source_examples']}+{row['official_examples']}/{row['source_conflicts']}"
        )
        if row["optional_capture_overlay"]:
            postal += "; capture"
        membership = {
            "canonical_country_reference": "country root",
            "administrative_roots": "ADM roots",
            "reference_root_only": "reference only; crosswalk gap",
            "missing_root": "missing root",
        }[row["membership"]]
        if row["selector"] != row["canonical"]:
            membership += f" ({len(row['membership_roots'])})"
        if row["requires_place_choice"]:
            membership += "; choice"
        phone = f"{row['phone_region']} +{row['calling_code']}" if row["phone_region"] else "unknown"
        values = [
            f"{row['selector']} / {row['label']}",
            row["canonical"],
            f"{row['format']} ({row['format_country']})",
            postal,
            f"{row['postal_subdivisions']:,}",
            f"{row['geo_administrative']:,} / {row['geo_localities']:,}",
            membership,
            phone,
            f"{row['zone_tab']} / {row['zone1970']}",
        ]
        lines.append("| " + " | ".join(cell(value) for value in values) + " |")
    lines += [
        "",
        "## Evidence and outstanding review",
        "",
        (
            "Verified by reproducible source builders/tests: canonical mapping and retired-code exclusion; source fingerprint checks; "
            "dedicated versus inherited/generic layouts; unchanged compiled postal patterns and conflict classification; namespaced postal subdivisions; "
            "positive unique GeoNames identities, bounded source parsing, explicit/derived same-country parent evidence and historical flags; "
            "direct phone regions and distinct IANA inventories. This document reads those artifacts; it does not replace their tests or assert that every record has been manually reviewed."
        ),
        "",
        (
            "Outstanding where applicable: national format/currentness and private-address policy; reviewed candidate graph/context membership (especially reference-only CP/CQ/DG); "
            "cross-border/ambiguous features, postcode conflicts or absent strict rules; actual listing timezone choices; number/provider capabilities; "
            "country/context activation and geocoder licensing/support. No row is promoted to a live-country approval by this report. "
            "A launch operator must record that decision against the actual country/context rules and imported graph, not edit this generated matrix."
        ),
        "",
        (
            "Source contracts, retained licenses and update commands: [identity sources](../resources/data/country-sources/README.md), "
            "[address provenance](../resources/data/addressing/manifest.v1.json), [postcode evidence](../resources/data/addressing/postal-evidence.v1.json), "
            "[GeoNames](../resources/data/geonames/README.md), "
            "[telephone reference](../resources/data/phone-metadata/README.md). "
            f"Versions: `{inputs['catalog']['version']}`; `{addresses['version']}`; `{geo['dataset_id']}`; `{phones['version']}`."
        ),
        "",
        "## Reproduce and detect stale evidence",
        "",
        "```sh",
        "python3 bin/build-country-readiness.py",
        "python3 bin/build-country-readiness.py --check",
        "python3 -m unittest discover -s tests -p test_country_readiness.py",
        "```",
        "",
        (
            "The generator is offline and deterministic. It checks matching catalog/full-bundle fingerprints and complete selector/canonical mappings; "
            "source changes require regeneration and diff review. The fingerprints below pin this report’s inputs; GeoNames shard hashes are pinned by its manifest."
        ),
        "",
        "| Input | SHA-256 |",
        "| --- | --- |",
    ]
    for key, path in INPUTS.items():
        lines.append(f"| [{Path(path).name}](../{path}) | `{hashes[key]}` |")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "docs/country-data-matrix.md")
    parser.add_argument(
        "--check", action="store_true", help="Fail if the retained matrix differs from current pinned inputs"
    )
    arguments = parser.parse_args()
    inputs, hashes = read_inputs()
    output = render(inputs, hashes)
    if arguments.check:
        require(
            arguments.output.is_file() and arguments.output.read_text(encoding="utf-8") == output,
            "Country data matrix is stale; rebuild and review the source diff",
        )
    else:
        arguments.output.write_text(output, encoding="utf-8")
    print("Country data matrix verified: 250 canonical identities, 257 selectors")


if __name__ == "__main__":
    main()
