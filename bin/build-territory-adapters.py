#!/usr/bin/env python3
"""Build resources/data/territory-adapters.v1.json from pinned data only.

A territory adapter says which places of the parent country make up an exceptional
CLDR selector (AC, TA, IC, EA, CQ, DG), which IANA zones apply there and which
rectangle limits address suggestions. Roots are reviewed GeoNames IDs listed below;
every other value is computed from the pinned GeoNames shards and tzdata zone.tab.

    python3 bin/build-territory-adapters.py          # write
    python3 bin/build-territory-adapters.py --check  # fail if the file is stale
"""

import gzip
import hashlib
import json
import sys
import tarfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "resources/data"
OUT = DATA / "territory-adapters.v1.json"
TZDATA = DATA / "country-sources/tzdata-2026e.tar.gz"

# Reviewed choices. 'roots' are the places a branch may sit in (with their descendants);
# 'extent' adds pinned points that only widen the suggestion rectangle; 'zone_comment'
# picks the parent's zone.tab row whose comment names the territory (None: the parent's
# only row). 'pad' is the margin in degrees around the pinned points.
SPEC = {
    "AC": {
        "country": "SH",
        "zone_comment": None,
        "areas": [{"name": "Ascension", "roots": {2411430: ("Ascension", "ADM1")}, "extent": {}, "pad": 0.05}],
    },
    "TA": {
        "country": "SH",
        "zone_comment": None,
        "areas": [
            {"name": "Tristan da Cunha", "roots": {3370684: ("Tristan da Cunha", "ADM1")}, "extent": {}, "pad": 0.05}
        ],
    },
    "IC": {
        "country": "ES",
        "zone_comment": "Canary Islands",
        "areas": [{"name": "Canary Islands", "roots": {2593110: ("Canary Islands", "ADM1")}, "extent": {}, "pad": 0.1}],
    },
    "EA": {
        "country": "ES",
        "zone_comment": "Ceuta, Melilla",
        "areas": [
            {"name": "Ceuta", "roots": {2519582: ("Ceuta", "ADM1")}, "extent": {}, "pad": 0.05},
            {"name": "Melilla", "roots": {6362988: ("Melilla", "ADM1")}, "extent": {}, "pad": 0.05},
        ],
    },
    "CQ": {
        "country": "GG",
        "zone_comment": None,
        "areas": [
            {"name": "Sark", "roots": {6696201: ("Sark", "PPL")}, "extent": {3042282: ("Sark", "ISL")}, "pad": 0.05}
        ],
    },
    "DG": {
        "country": "IO",
        "zone_comment": None,
        "areas": [
            {
                "name": "Diego Garcia",
                "roots": {7503195: ("Downtown", "PPLL"), 13631478: ("Seabreeze village", "PPLL")},
                "extent": {
                    1282575: ("Diego Garcia", "ATOL"),
                    1282544: ("Minni Minni", "PPLQ"),
                    6904652: ("Carcasse", "PPLQ"),
                    6904653: ("East Point Settlement", "PPLQ"),
                },
                "pad": 0.1,
            }
        ],
    },
}
EXCLUDED = {
    "CP": "Clipperton Island is uninhabited, has no populated place in the pinned GeoNames data and no IANA zone "
    "(FR zone.tab lists only Europe/Paris).",
}


def fail(message):
    sys.exit("territory adapters: " + message)


def zone_tab():
    with tarfile.open(TZDATA) as tar:
        text = tar.extractfile("zone.tab").read().decode()
    rows = defaultdict(list)
    for line in text.splitlines():
        if line and not line.startswith("#"):
            parts = line.split("\t")
            rows[parts[0]].append({"zone": parts[2], "comment": parts[3] if len(parts) > 3 else None})
    return rows


def shard(country, manifest):
    entry = next(s for s in manifest["shards"] if s["country_code"] == country)
    with gzip.open(DATA / "geonames" / entry["path"]) as f:
        rows = [json.loads(line) for line in f]
    return {r["geoname_id"]: r for r in rows}, entry["sha256"]


def build():
    manifest = json.loads((DATA / "geonames/manifest.json").read_text())
    zones = zone_tab()
    out = {
        "schema_version": 1,
        "version": "territory-adapters-2026-11-09",
        "sources": {
            "geonames_dataset": manifest["dataset_id"],
            "tzdata": "tzdata-2026e zone.tab",
            "tzdata_sha256": hashlib.sha256(TZDATA.read_bytes()).hexdigest(),
            "shards": {},
        },
        "rect_order": "min_lon,min_lat,max_lon,max_lat",
        "selectors": {},
        "excluded": EXCLUDED,
    }
    for selector, spec in SPEC.items():
        country = spec["country"]
        places, digest = shard(country, manifest)
        out["sources"]["shards"][country] = digest
        children = defaultdict(list)
        for r in places.values():
            for parent in r.get("parent_geoname_ids") or []:
                children[parent].append(r["geoname_id"])
        rows = zones[country]
        picked = [r for r in rows if r["comment"] == spec["zone_comment"]] if spec["zone_comment"] else rows
        if len(picked) != 1:
            fail(f"{selector}: expected one {country} zone.tab row, found {len(picked)}")
        areas = []
        for area in spec["areas"]:
            points = []
            for gid, (name, code) in {**area["roots"], **area["extent"]}.items():
                r = places.get(gid)
                if not r or r["name"] != name or r["feature_code"] != code:
                    fail(f"{selector}: GeoNames {gid} is not {name} ({code}) in the pinned {country} shard")
                stack = [gid] if gid in area["roots"] else []
                points.append(r)
                while stack:
                    for child in children[stack.pop()]:
                        points.append(places[child])
                        stack.append(child)
            pad = area["pad"]
            lats = [p["latitude"] for p in points]
            lons = [p["longitude"] for p in points]
            areas.append(
                {
                    "name": area["name"],
                    "root_geoname_ids": sorted(area["roots"]),
                    "pinned_points": len(points),
                    "rect": [
                        round(min(lons) - pad, 4),
                        round(min(lats) - pad, 4),
                        round(max(lons) + pad, 4),
                        round(max(lats) + pad, 4),
                    ],
                    "padding_degrees": pad,
                }
            )
        out["selectors"][selector] = {
            "country_code": country,
            "provider_country": country.lower(),
            "timezones": [picked[0]["zone"]],
            "timezone_basis": f"zone.tab {country} row"
            + (f" '{spec['zone_comment']}'" if spec["zone_comment"] else " (the only row)"),
            "areas": areas,
        }
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    text = build()
    if "--check" in sys.argv:
        if OUT.read_text() != text:
            fail("stale; rerun bin/build-territory-adapters.py")
        print("territory adapters up to date")
    else:
        OUT.write_text(text)
        print("wrote", OUT.relative_to(ROOT))
