#!/usr/bin/env python3
"""Build pinned postal-reference data, offline by default. Never activates a country.

Postal subdivisions are source-specific mailing choices, not ISO subdivisions or
GeoNames boundaries. Recipient requirements stay labelled as shipping metadata.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tarfile
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "resources/data"
SOURCES = DATA / "addressing"
COMMIT = "e3ce66714cfa181b848533d926e8583261253c9e"
ARCHIVE = "commerceguys-e3ce667.tar.gz"
ARCHIVE_SHA = "01bd43057c0766e4ec21e687944abf7d4f0baa2df81b975bcd0b9004999faabd"
GOOGLE_COMMIT = "81eb9628382b07d371d8ea0b11badf7de3857fd5"
GOOGLE_SHA = "51a5da9ac621f3457b96b99de798a47a02004f57e4289c1dd587a95730dad720"
GOOGLE_LICENSE_SHA = "389e6d12ea7853b6e9d797a98d19ddc6ccfaa021f29e21b2ac1ebc68c2607280"
POSTAL_EVIDENCE_SHA = "545de979bd1fb8c7c938006d6e72697277a4d4bdf56f7993064be125ba0ff1a1"
PERSONAL_FIELDS = {"givenName", "additionalName", "familyName", "organization"}
PARENT_FORMATS = {"CP": "FR", "CQ": "GG", "DG": "IO", "EA": "ES", "IC": "ES"}
FIELD_MAP = {
    "addressLine1": "line1",
    "addressLine2": "line2",
    "addressLine3": "line3",
    "administrativeArea": "postal_admin_text",
    "locality": "postal_locality",
    "dependentLocality": "sublocality",
    "postalCode": "postal_code",
    "sortingCode": "sorting_code",
}
OVERLAYS = {
    "CD": (
        "Seven-digit postcode and province/dependent-rural-locality capture.",
        "codEn.pdf",
        "2022-09",
    ),
    "DJ": (
        "Five-digit postcode capture; locality and region remain distinct.",
        "djiEn.pdf",
        "2020-05",
    ),
    "GH": (
        "Capture postcode and longer digital address separately; do not truncate either.",
        "ghaEn.pdf",
        None,
    ),
    "GY": (
        "Capture postcode; source header says seven digits but example has six. No strict length.",
        "guyEn.pdf",
        None,
    ),
    "LC": (
        "Capture LC-prefixed postcode and preserve original spacing.",
        "lcaEn.pdf",
        None,
    ),
    "MS": ("Capture MSR-prefixed postcode.", "msrEn.pdf", None),
    "NU": (
        "Capture four-digit territory postal code without changing the NU identity.",
        "niuEn.pdf",
        None,
    ),
    "PS": (
        "Capture complete or partial alphanumeric postal value; never invent missing suffixes.",
        "pseEn.pdf",
        None,
    ),
    "TL": ("Capture TL-prefixed postal code; preserve raw spacing.", "tlsEn.pdf", None),
    "TT": ("Capture six-digit postcode with locality context.", "ttoEn.pdf", "2014-05"),
    "UG": (
        "Capture five-digit postcode for urban/rural and PO-box addresses.",
        "ugaEn.pdf",
        "2026-01",
    ),
    "WS": (
        "Capture WS-prefixed postcode and retain island/locality distinctions.",
        "wsmEn.pdf",
        "2014-05",
    ),
}

PHP_EXPORT = r"""<?php
$root=$argv[1];$codes=json_decode(stream_get_contents(STDIN),true,512,JSON_THROW_ON_ERROR);
spl_autoload_register(static function(string $name)use($root):void{
    $prefix='CommerceGuys\\Addressing\\';
    if(str_starts_with($name,$prefix))require $root.'/src/'.str_replace('\\','/',substr($name,strlen($prefix))).'.php';
});
$repository=new class extends CommerceGuys\Addressing\AddressFormat\AddressFormatRepository {
    public function rawDefinitions():array{return $this->getDefinitions();}
};
$definitions=$repository->rawDefinitions();
$dedicated=array_keys($repository->getAll());$result=[];
foreach($codes as $code){$f=$repository->get($code);$result[$code]=[
    'country_code'=>$code,'format'=>$f->getFormat(),'local_format'=>$f->getLocalFormat(),
    'source_has_explicit_format'=>array_key_exists('format',$definitions[$code]??[]),
    'locale'=>$f->getLocale(),'used_fields'=>$f->getUsedFields(),
    'required_fields'=>$f->getRequiredFields(),'uppercase_fields'=>$f->getUppercaseFields(),
    'default_values'=>$f->getDefaultValues(),'administrative_area_type'=>$f->getAdministrativeAreaType(),
    'locality_type'=>$f->getLocalityType(),'dependent_locality_type'=>$f->getDependentLocalityType(),
    'postal_code_type'=>$f->getPostalCodeType(),'postal_code_pattern'=>$f->getPostalCodePattern(),
    'postal_code_prefix'=>$f->getPostalCodePrefix(),'subdivision_depth'=>$f->getSubdivisionDepth(),
    'subdivision_data_fields'=>$f->getSubdivisionDataFields(),
];}
echo json_encode(['dedicated'=>$dedicated,'formats'=>$result],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_THROW_ON_ERROR);
"""
PHP_PATTERNS = r"""<?php
$items=json_decode(stream_get_contents(STDIN),true,512,JSON_THROW_ON_ERROR);$out=[];
foreach($items as $code=>$x){$p=$x['pattern'];$matches=[];$valid=null;
if($p!==null&&$p!==''){$regex='~\\A(?:'.str_replace('~','\\~',$p).')\\z~uD';$valid=@preg_match($regex,'')!==false;
foreach($x['examples'] as $example)$matches[$example]=$valid?preg_match($regex,$example)===1:null;}
$out[$code]=['pattern_compiles'=>$valid,'examples'=>(object)$matches];}
echo json_encode($out,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_THROW_ON_ERROR);
"""


def canonical_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode()


def checked(path: Path, expected: str) -> bytes:
    payload = path.read_bytes()
    actual = hashlib.sha256(payload).hexdigest()
    if actual != expected:
        raise ValueError(f"Pinned source checksum mismatch: {path.name}")
    return payload


def download(url: str, path: Path, expected: str, maximum: int) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "country-place-matrix-builder"})
    with urllib.request.urlopen(request, timeout=60) as response:
        body = response.read(maximum + 1)
    if len(body) > maximum or hashlib.sha256(body).hexdigest() != expected:
        raise ValueError(f"Unexpected source size or checksum: {path.name}")
    path.write_bytes(body)


def extract(archive: Path, destination: Path) -> Path:
    prefix = "addressing-" + COMMIT
    with tarfile.open(archive) as stream:
        members = stream.getmembers()
        if sum(member.size for member in members) > 32 * 1024 * 1024:
            raise ValueError("Address source exceeds extraction budget")
        for member in members:
            path = Path(member.name)
            if (
                path.is_absolute()
                or ".." in path.parts
                or path.parts[0] != prefix
                or member.issym()
                or member.islnk()
                or not (member.isdir() or member.isfile())
            ):
                raise ValueError("Unsafe addressing archive entry")
        stream.extractall(destination, filter="data")
    return destination / prefix


def php(script: str, data, *arguments):
    with tempfile.TemporaryDirectory(prefix="cpm-address-export-") as temporary:
        path = Path(temporary) / "export.php"
        path.write_text(script)
        result = subprocess.run(
            ["php", str(path), *map(str, arguments)],
            input=json.dumps(data),
            text=True,
            capture_output=True,
            check=True,
            timeout=60,
        )
        return json.loads(result.stdout)


def google_records(path: Path) -> dict:
    records = {}
    for line in path.read_text().splitlines():
        key, value = line.split("=", 1)
        if re.fullmatch(r"data/[A-Z]{2}", key):
            record = json.loads(value)
            if key[5:] in records:
                raise ValueError("Duplicate Google country root")
            records[key[5:]] = record
    return records


def add_official_examples(selectors: dict, evidence: dict) -> None:
    """Enrich hints without repairing raw sources or weakening their patterns."""
    candidates = {}
    for code, item in selectors.items():
        examples = evidence["countries"].get(code, {}).get("examples", [])
        candidates[code] = {
            "pattern": item["postal_code_pattern"],
            "examples": [entry["value"] for entry in examples],
        }
    checks = php(PHP_PATTERNS, candidates)
    for code, item in selectors.items():
        country_evidence = evidence["countries"].get(code, {})
        official = []
        for example in country_evidence.get("examples", []):
            if example["evidence_key"] not in evidence["sources"]:
                raise ValueError("Missing official postal example provenance: " + code)
            if checks[code]["examples"].get(example["value"]) is not True:
                raise ValueError("Official example conflicts with unchanged postal pattern: " + code)
            official.append(
                {
                    **example,
                    "source_key": "official_postal_reference_examples",
                }
            )
        item["official_postal_code_examples"] = official
        item["postal_code_examples_display"] = list(
            dict.fromkeys(item["postal_code_examples_valid"] + [example["value"] for example in official])
        )
        item["postal_source_review_notes"] = country_evidence.get("notes", [])


def subdivision_rows(root: Path, formats: dict) -> tuple[list, list]:
    rows = []
    roots = []
    seen = set()
    for path in sorted((root / "resources/subdivision").glob("*.json")):
        body = json.loads(path.read_text())
        country = body["country_code"]
        parents = body.get("parents", [country])
        if parents[0] != country:
            raise ValueError("Subdivision parent country mismatch")
        if len(parents) == 1:
            roots.append(country)
        fields = formats[country]["subdivision_data_fields"]
        role = fields[len(parents) - 1] if len(parents) - 1 < len(fields) else None
        for key, entry in body["subdivisions"].items():
            raw = entry or {}
            source_path = [*parents, key]
            identity = json.dumps(source_path, ensure_ascii=False, separators=(",", ":"))
            if identity in seen:
                raise ValueError("Duplicate postal subdivision path")
            seen.add(identity)
            routing_only = (
                country == "US" and source_path[1] in {"AS", "FM", "GU", "MH", "MP", "PW", "PR", "VI", "AA", "AE", "AP"}
            ) or (country == "CN" and source_path[1] in {"HK", "MO", "TW"})
            rows.append(
                {
                    "source_key": "commerceguys_addressing",
                    "namespace": "postal_subdivision",
                    "source_namespace": "commerceguys_postal",
                    "source_id": hashlib.sha256(identity.encode()).hexdigest(),
                    "source_path": source_path,
                    "country_code": country,
                    "code": str(raw.get("code", key)),
                    "parent_code": parents[-1] if len(parents) > 1 else None,
                    "path": source_path[1:],
                    "role": role,
                    "name": raw.get("name", key),
                    "local_code": raw.get("local_code"),
                    "local_name": raw.get("local_name"),
                    "locale": body.get("locale"),
                    "postal_code_pattern": raw.get("postal_code_pattern"),
                    "has_children": bool(raw.get("has_children", False)),
                    "routing_only": routing_only,
                    "geographic_membership_approved": False,
                }
            )
    return rows, sorted(roots)


def build() -> dict:
    archive = SOURCES / ARCHIVE
    checked(archive, ARCHIVE_SHA)
    checked(SOURCES / "google-countryinfo.txt", GOOGLE_SHA)
    checked(SOURCES / "google-libaddressinput-LICENSE", GOOGLE_LICENSE_SHA)
    evidence = json.loads(checked(SOURCES / "postal-evidence.v1.json", POSTAL_EVIDENCE_SHA))
    catalog = json.loads((DATA / "country-catalog.v1.json").read_text())
    canonical = set(catalog["countries"])
    selector_codes = set(catalog["selectors"])
    with tempfile.TemporaryDirectory(prefix="cpm-addressing-") as temporary:
        source = extract(archive, Path(temporary))
        exported = php(PHP_EXPORT, sorted(canonical | selector_codes), source)
        formats = exported["formats"]
        dedicated = set(exported["dedicated"])
        subdivisions, roots = subdivision_rows(source, formats)
        (SOURCES / "commerceguys-LICENSE").write_bytes((source / "LICENSE").read_bytes())
    records = google_records(SOURCES / "google-countryinfo.txt")
    google_ref = json.loads((SOURCES / "google-source-ref.json").read_text())
    sources = [
        {
            "key": "commerceguys_addressing",
            "revision": COMMIT,
            "release": "v2.3.2",
            "released_at": "2026-10-09",
            "license": "MIT",
            "url": "https://codeload.github.com/commerceguys/addressing/tar.gz/" + COMMIT,
            "file": "resources/data/addressing/" + ARCHIVE,
            "sha256": ARCHIVE_SHA,
        },
        {
            "key": "google_libaddressinput_examples",
            "revision": GOOGLE_COMMIT,
            "data_last_change_commit": google_ref["data_last_change_commit"],
            "data_last_change_at": google_ref["data_last_change_at"],
            "license": "Apache-2.0; bundled third-party notices retained",
            "url": "https://raw.githubusercontent.com/google/libaddressinput/"
            + GOOGLE_COMMIT
            + "/testdata/countryinfo.txt",
            "file": "resources/data/addressing/google-countryinfo.txt",
            "sha256": GOOGLE_SHA,
        },
        {
            "key": "official_postal_reference_examples",
            "revision": "reviewed-2026-10-27-" + POSTAL_EVIDENCE_SHA[:12],
            "license": "Minimal factual reference observations; publisher attribution retained; full documents not redistributed",
            "file": "resources/data/addressing/postal-evidence.v1.json",
            "sha256": POSTAL_EVIDENCE_SHA,
            "source_urls_in": "sources.*.url",
        },
    ]
    countries = {}
    for code in sorted(canonical):
        item = dict(formats[code])
        item.update(
            {
                "format_key": code,
                "format_status": "dedicated" if code in dedicated else "generic",
                "source_key": "commerceguys_addressing",
                "source_shipping_required_fields": list(item["required_fields"]),
                "directory_required_fields": [x for x in item["required_fields"] if x not in PERSONAL_FIELDS],
                "source_used_fields": list(item["used_fields"]),
                "postal_code_examples": [x for x in records.get(code, {}).get("zipex", "").split(",") if x],
                "postal_code_examples_source": (
                    "google_libaddressinput_examples" if records.get(code, {}).get("zipex") else None
                ),
                "overlays": [],
                "subdivision_root_available": code in roots,
                "reference_only": True,
                "public_activation_approved": False,
                "postal_code_status_scope": "source_format_not_national_absence",
            }
        )
        item["postal_code_status"] = (
            "pattern"
            if item["postal_code_pattern"]
            else (
                "not_used"
                if item["source_has_explicit_format"] and "postalCode" not in item["source_used_fields"]
                else "unknown"
            )
        )
        if code in OVERLAYS:
            note, pdf, revision = OVERLAYS[code]
            if "postalCode" not in item["used_fields"]:
                item["used_fields"].append("postalCode")
            item["postal_code_status"] = "unknown"
            item["postal_code_pattern"] = None
            item["directory_required_fields"] = [x for x in item["directory_required_fields"] if x != "postalCode"]
            item["overlays"] = [
                {
                    "kind": "optional_postcode_capture",
                    "source": "UPU country addressing sheet, content reviewed 2026-10-25",
                    "source_url": "https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/" + pdf,
                    "source_printed_revision": revision,
                    "review_record": "spec/countries/fallback-address-review.md",
                    "note": note,
                    "strict_pattern_approved": False,
                    "required": False,
                    "format_order_approved": False,
                }
            ]
        countries[code] = item
    selectors = {}
    for selector in sorted(selector_codes):
        canonical_code = catalog["selectors"][selector]["country_code"]
        format_key = PARENT_FORMATS.get(selector, selector)
        item = dict(formats[format_key])
        item.update(
            {
                "selector_code": selector,
                "country_code": canonical_code,
                "format_key": format_key,
                "format_status": (
                    "parent" if format_key != selector else ("dedicated" if selector in dedicated else "generic")
                ),
                "requires_context_review": True,
                "reference_only": True,
                "public_activation_approved": False,
                "source_key": "commerceguys_addressing",
                "overlays": [],
            }
        )
        if selector == canonical_code:
            item.update(countries[canonical_code])
            item["selector_code"] = selector
        elif selector in {"AC", "TA"}:
            item["postal_code_examples"] = [x for x in records.get(selector, {}).get("zipex", "").split(",") if x]
            item["postal_code_status"] = "pattern" if item["postal_code_pattern"] else "unknown"
            item["directory_required_fields"] = [x for x in item["required_fields"] if x not in PERSONAL_FIELDS]
        else:
            item.update(
                {
                    "postal_code_examples": countries[format_key]["postal_code_examples"],
                    "postal_code_status": countries[format_key]["postal_code_status"],
                    "directory_required_fields": countries[format_key]["directory_required_fields"],
                    "parent_format_source": "spec/countries/mapping-exceptions.md",
                    "parent_format_requires_territory_review": True,
                }
            )
        item["format_country_code"] = format_key
        item.setdefault("source_used_fields", list(item["used_fields"]))
        item.setdefault("source_shipping_required_fields", list(item["required_fields"]))
        item.setdefault("postal_code_status_scope", "source_format_not_national_absence")
        selectors[selector] = item
    checks = php(
        PHP_PATTERNS,
        {
            code: {
                "pattern": item["postal_code_pattern"],
                "examples": item.get("postal_code_examples", []),
            }
            for code, item in selectors.items()
        },
    )
    for code, item in selectors.items():
        check = checks[code]
        if check["pattern_compiles"] is False:
            raise ValueError("Uncompilable postal pattern " + code)
        item["postal_pattern_compiles"] = check["pattern_compiles"]
        item["postal_code_examples_valid"] = [x for x, v in check["examples"].items() if v is True]
        item["source_example_conflicts"] = [x for x, v in check["examples"].items() if v is False]
        if code in countries:
            for key in [
                "postal_pattern_compiles",
                "postal_code_examples_valid",
                "source_example_conflicts",
            ]:
                countries[code][key] = item[key]
    add_official_examples(selectors, evidence)
    for code, item in selectors.items():
        if code in countries:
            for key in [
                "official_postal_code_examples",
                "postal_code_examples_display",
                "postal_source_review_notes",
            ]:
                countries[code][key] = item[key]
    for selector, item in selectors.items():
        if selector != item["country_code"]:
            item["address_reference"] = dict(item)
    return {
        "schema_version": 1,
        "version": "commerceguys-"
        + COMMIT[:12]
        + "-google-"
        + GOOGLE_COMMIT[:12]
        + "-postal-"
        + POSTAL_EVIDENCE_SHA[:12]
        + "-v1",
        "country_catalog_version": catalog["version"],
        "country_catalog_sha256": hashlib.sha256((DATA / "country-catalog.v1.json").read_bytes()).hexdigest(),
        "sources": sources,
        "field_roles": FIELD_MAP,
        "countries": countries,
        "selectors": selectors,
        "subdivisions": subdivisions,
        "coverage": {
            "canonical_countries": len(countries),
            "selectors": len(selectors),
            "upstream_dedicated_formats": len(dedicated),
            "canonical_dedicated_formats": sum(x["format_status"] == "dedicated" for x in countries.values()),
            "selector_dedicated_formats": sum(x["format_status"] == "dedicated" for x in selectors.values()),
            "parent_formats": sorted(PARENT_FORMATS),
            "generic_selectors": [c for c, x in selectors.items() if x["format_status"] == "generic"],
            "postal_capture_overlays": sorted(OVERLAYS),
            "subdivision_roots": roots,
            "subdivision_records": len(subdivisions),
            "countries_with_source_examples": sum(bool(x["postal_code_examples"]) for x in countries.values()),
            "countries_with_validated_source_examples": sum(
                bool(x["postal_code_examples_valid"]) for x in countries.values()
            ),
            "countries_with_official_examples": [
                code for code, item in countries.items() if item["official_postal_code_examples"]
            ],
            "countries_with_display_examples": sum(bool(x["postal_code_examples_display"]) for x in countries.values()),
            "source_example_conflicts": {
                c: x["source_example_conflicts"] for c, x in countries.items() if x["source_example_conflicts"]
            },
            "national_or_provider_acceptance_claimed": False,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    SOURCES.mkdir(parents=True, exist_ok=True)
    if args.fetch:
        download(
            "https://codeload.github.com/commerceguys/addressing/tar.gz/" + COMMIT,
            SOURCES / ARCHIVE,
            ARCHIVE_SHA,
            32 * 1024 * 1024,
        )
        download(
            "https://raw.githubusercontent.com/google/libaddressinput/" + GOOGLE_COMMIT + "/testdata/countryinfo.txt",
            SOURCES / "google-countryinfo.txt",
            GOOGLE_SHA,
            4 * 1024 * 1024,
        )
        download(
            "https://raw.githubusercontent.com/google/libaddressinput/" + GOOGLE_COMMIT + "/LICENSE",
            SOURCES / "google-libaddressinput-LICENSE",
            GOOGLE_LICENSE_SHA,
            1024 * 1024,
        )
    result = build()
    body = canonical_bytes(result)
    destination = DATA / "country-addresses.v1.json"
    digest = hashlib.sha256(body).hexdigest()
    # The runtime index excludes mailing subdivision rows, but is tied to the
    # exact distributable full bundle; import tools still read the full source.
    metadata = {key: value for key, value in result.items() if key != "subdivisions"}
    metadata["full_bundle_sha256"] = digest
    metadata["full_bundle_file"] = "resources/data/country-addresses.v1.json"
    outputs = {
        destination: body,
        DATA / "country-addresses.v1.sha256": (digest + "\n").encode(),
    }
    metadata_body = canonical_bytes(metadata)
    outputs[DATA / "country-address-metadata.v1.json"] = metadata_body
    outputs[DATA / "country-address-metadata.v1.sha256"] = (hashlib.sha256(metadata_body).hexdigest() + "\n").encode()
    manifest = {
        "schema_version": 1,
        "version": result["version"],
        "sources": result["sources"],
        "source_release_verification": {
            "repository": "commerceguys/addressing",
            "tag": "v2.3.2",
            "commit": COMMIT,
            "committed_at": "2026-10-09T10:50:35Z",
        },
        "google_source_ref": json.loads((SOURCES / "google-source-ref.json").read_text()),
        "licenses": [
            {
                "file": "resources/data/addressing/" + name,
                "sha256": hashlib.sha256((SOURCES / name).read_bytes()).hexdigest(),
            }
            for name in ["commerceguys-LICENSE", "google-libaddressinput-LICENSE"]
        ],
        "outputs": [
            {
                "file": str(path.relative_to(ROOT)),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
            }
            for path, payload in outputs.items()
            if path.suffix == ".json"
        ],
        "coverage": result["coverage"],
        "update_policy": "Review official upstream release, license and source changes; update pinned hashes deliberately; rebuild offline; run country-address reference and integration tests. Never activate countries from a source update.",
        "limitations": [
            "Postal subdivision identifiers are not ISO/FIPS/GeoNames geographic boundaries.",
            "A generic format is an explicit fallback, not national validation.",
            "UPU overlays preserve optional capture only; no invented postcode pattern or requiredness.",
            "Source examples conflicting with newer patterns remain recorded but are excluded from validated hints.",
            "Reference imports do not establish national, provider, legal or publication acceptance.",
        ],
    }
    outputs[SOURCES / "manifest.v1.json"] = canonical_bytes(manifest)
    for path, payload in outputs.items():
        if args.check:
            if not path.exists() or path.read_bytes() != payload:
                raise SystemExit("Country address artifact is not reproducible: " + str(path.relative_to(ROOT)))
        else:
            path.write_bytes(payload)
    print(json.dumps(result["coverage"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
