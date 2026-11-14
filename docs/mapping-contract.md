# Country mappings and geographic reconciliation

[Per-country matrix](mapping-matrix.md) · [Country cases](mapping-exceptions.md) · [Source evidence](source-evidence.md)

## Scope and status

This document checks **every candidate against the actual source files**, defines how the sources join, and records specific national exceptions. It does not certify every address, current local boundary or geocoder response.

Working approach: one shared form and resolver driven by reviewed country rules, with small explicit exceptions. Keep postal formatting, administrative membership and service coverage distinct. Do not build a universal State → County → City hierarchy, and do not generate hundreds of unrelated forms.

## Findings from the source cross-check

| Finding | Required correction |
| --- | --- |
| Existing 256-entry catalogue omits `CQ` (Sark), present in pinned CLDR 49 | Inventory now has 257 candidates; CQ needs an explicit territory/format/provider rule, not an invented ordinary ISO country |
| 206 dedicated address definitions; 51 candidates lack one after adding CQ | No generic-format candidate is automatically ready; [46 country postal references were read](fallback-address-review.md), revealing at least 12 missing postcode fields and source inconsistencies |
| Actual library tree has 63 country subdivision roots; README advertises 62 | Use inspected file coverage and field roles, not the advertised count; 194 candidates have no root file |
| ZA has no library subdivision root and its postal template omits province | Supply reviewed province browse data separately; do not infer that South Africa has no provinces or require province in its postal template |
| GB's 217-entry address subdivision list includes Cumbria and lacks the new Cumberland/Westmorland and Furness entries | It cannot be our current local-authority hierarchy; use dated national authority data and keep postal/historic geography separate |
| HK library root has three address areas; GeoNames has 18 first-level districts | Preserve area → district relationships; neither is a replacement for the other |
| IE library has 26 address counties; GeoNames has four first-level provinces and 31 second-level areas | Label/namespace each structure; never join by level number |
| US library root has 62 mailing choices, including military codes and other country/territory codes | Separate postal routing choices from actual branch countries/states |
| GeoNames country file retains obsolete `AN` and `CS`; most ADM1 codes use FIPS | Exclude obsolete country entries from new selection; never treat a GeoNames key as an ISO subdivision code |
| Ten candidates have no own row in IANA zone.tab | This is a mapping gap, not permission to assume UTC or a parent country's first zone |

Counts are source observations dated 25 October 2026. The [matrix](mapping-matrix.md) records all 257 rows; [evidence](source-evidence.md) pins versions/hashes and explains what was actually checked.

## Minimal canonical records

| Field/relation | Meaning |
| --- | --- |
| `country_code` | Reviewed canonical country/territory jurisdiction; ordinary assigned ISO alpha-2 where applicable, explicit exceptional-code policy where not |
| `territory_code` | Optional distinct island/territory selector within a canonical country; never a second listing identity |
| `postal_format_code` | Reviewed address-rule key; may differ from canonical country for a special territory; never chosen from postcode alone |
| `place_id` | Stable internal locality/area identity, with typed current memberships and one useful browse path |
| Source reference | Namespace + version + external ID/code; e.g. GeoNames geoname ID and ADM key are distinct from ISO or ONS codes |
| Postal text | Address lines, dependent locality, post town/locality, optional postal administrative text, postcode/sorting code where used; preserve original supplied spelling separately |
| Timezone | Valid IANA identifier confirmed for the branch; independent of country default, language, currency and current UTC offset |

Use existing place/relation tables and explicit country overrides; no graph database or third mapping service. A locality may overlap more than one administrative area; a simplified browse path must not erase its other evidenced memberships. Country subdivisions, postal routing and statistical areas keep their actual types/effective dates.

Working special-code treatment is in [the exception table](mapping-exceptions.md): seven CLDR territory selectors resolve to country plus territory context; `XK` needs explicit non-ISO handling. These are documented product mappings, not claims that CLDR defines political sovereignty. Keep provider-specific mappings separate and confirm disputed/changing jurisdictions before activation. A source code must never silently move an owner's address.

## Joining and updating sources

1. Select a reviewed country/territory context before interpreting other fields. Only declared aliases normalise; `UK` can suggest GB, while `SA` remains Saudi Arabia and `NA` remains Namibia. Preserve numeric/postal codes as strings, including leading zeros.
2. Resolve namespaced source IDs through a reviewed crosswalk. Match country, actual area type, dated parents and source meaning. Never join on a bare code, same display name, ADM number or shared calling code.
3. Where no crosswalk exists, retain candidate text/source facts and queue review. Name matching can suggest candidates within checked context; it cannot publish a new global place or choose the first match. Store provenance/uncertainty explicitly.
4. A provider `state`, `county`, `city` or `district` is a proposed component. Apply that country's mapping rules; do not copy keys wholesale into canonical roles. Check selected territory/country and precision, then require owner confirmation. An approximate point is not a street address or a boundary.
5. Source changes produce a reviewed diff: additions, renames, retired codes, boundary changes and one-to-many splits. Retain internal IDs and dated aliases where identity continues; record successors and review affected listings/service areas when it does not. No wholesale ID replacement or automatic historic-to-current relocation.

GeoNames inspection found 3,865 ADM1 and 47,764 ADM2 records, with every ADM2 key having a corresponding ADM1 key. This is a structural check only: level completeness, current boundaries, official names and populated locality membership still need national review. Seed counts are never advertised as authoritative coverage.
