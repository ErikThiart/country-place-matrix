# GeoNames reference snapshot

**In this repository the `shards/` directory is not included** (about 250 MB). `manifest.json` and `sources.json` are kept, which is all the matrix needs. Rebuild the shards from the pinned GeoNames downloads with `python3 bin/build-geonames-reference.py --fetch`. Statements below that the snapshot is retained in Git describe the original working repository.

This directory retains licensed real geographic reference data for candidate imports. It does **not** enable a country, replace a reviewed current geography graph, validate a business address, or prove worldwide national/postal completeness.

## Contents and provenance

- `sources.json` pins six official GeoNames downloads to 27 October 2026 with URL, source modification time, byte length and SHA-256.
- `GEONAMES-README.txt` retains upstream field definitions, attribution and licensing. Data is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); attribute **GeoNames, https://www.geonames.org/**. GeoNames explicitly disclaims accuracy, timeliness and completeness.
- `manifest.json` records source coverage, exclusions, review flags, parent evidence, country/selector roots and each shard's checksum, size, feature counts and record count.
- `shards/CC-NNN.ndjson.gz` contains all available source administrative (`A`) and populated (`P`) features in the canonical country inventory, plus named exceptional territory roots. This includes rural and zero-population records; it is not the population-threshold `cities500` subset. Source population zero may mean unknown.

Raw archives are retained outside Git in `var/reference-sources/geonames/2026-10-27/`. `allCountries.zip` is 422,503,902 bytes and contains a 1,790,770,164-byte text member; the builder streams it without extracting it. The full normalized snapshot is retained in Git. Daily upstream URLs are mutable: a future download is **not** a reproducible replacement unless its pinned hash matches. Preserve the raw cache for exact source rebuilding; a changed upstream snapshot requires a separately reviewed revision and source lock update.

## Rebuild and verification

From the repository root:

```sh
python3 bin/build-geonames-reference.py
python3 -m unittest discover -s tests -p test_geonames_reference.py -v
```

`--fetch` retrieves only missing exact pinned inputs and rejects upstream byte/hash changes. It makes no authenticated/provider request. `--cache`, `--output` and `--catalog` select explicit local paths. Keep `sources.json` in the output directory. Allow at least 1 GB temporary free space for raw inputs plus an atomic normalized-shard rebuild; each committed shard is below 95 MiB and contains at most 100,000 records.

The builder validates strict UTF-8, nineteen-field shape, positive bounded source identities, duplicate identities across the complete source archive, finite/ranged retained coordinates and bounded archive/line sizes. It reads complete compressed members so ZIP CRC checks apply. Output gzip timestamps/filenames are fixed; identical input bytes produce identical shards. Record order follows the pinned source snapshot; identifiers and parent lookup do not depend on ordering. Tests check all committed shard byte lengths/hashes and country/selector inventories, real records from all countries, exact exceptional roots and isolated malformed/historical/parent/determinism regressions.

## Identity and parent contract

`geoname_id` is the stable numeric source identity in namespace `geonames:feature`; `source_key` is `geonames:<id>`. Country identities remain the existing canonical 249 ISO identities plus explicit non-ISO `XK`. GeoNames country names/alpha-3/numeric values never overwrite that catalog. Obsolete `AN`, `CS`, `YU` and unassigned source codes are excluded and counted, never assigned a guessed successor.

`admin1_code` through `admin4_code` and `admin_code_key` are **GeoNames/FIPS administration codes, not ISO subdivision codes**. Feature class/code are retained; do not infer a universal state/county/city model from their level. `PPLX` remains a neighbourhood feature, not a verified independent city. Historical, abandoned and destroyed feature categories remain reference records with `current_selectable: false` and a review flag. Overlong names remain intact and require review rather than silent truncation.

`browse_parent_geoname_id` supplies one deterministic browse parent. `parent_geoname_ids` retains up to eight eligible administrative edges. `parent_source` distinguishes:

- `geonames_hierarchy`: explicit source `ADM` edges to current same-country administrative features with strictly decreasing level.
- `derived_admin_codes`: an exact same-source, same-country administrative-code join. Ambiguous code keys are excluded from this lookup.
- `country_only`: no more specific resolved parent; this is broad canonical-country containment, not a verified locality relationship.
- `unknown`: no resolved parent; review is required.

A source hierarchy with several same-level parents is flagged; no arbitrary source-edge order chooses a parent. Root/administrative level strictly decreases to prevent derived administrative cycles. These candidate relations are not boundary polygons, address validation or political-boundary adjudication.

`current_selectable` describes source category and name-length eligibility **only**. Importers must preserve current authorization, country policy, source review, graph review and publication rules. Moving a stable source identity to another country requires explicit reconciliation, not an in-place foreign-key reassignment.

## Names, timezones and exceptional selectors

`name` is the source primary name; `ascii_name` is explicitly ASCII, not a native name. Up to 64 unique **untagged** alternate names are retained along with their full source count; additional names remain in the pinned raw archive and trigger a flag. No language, official-name, translated-name or native-name status is invented. Localized/native display needs a separately licensed, language-tagged name source.

The source timezone is retained when present and mapped against the existing pinned IANA identity catalog when known. Missing/unknown zones remain null/flagged. A feature centroid timezone is a candidate, not proof of a timezone boundary and never an automatic listing timezone default.

The 257 selector contexts map to 250 canonical identities. The manifest records explicit source roots for Ascension, Tristan da Cunha, the Canary Islands and the separate **ADM1 Ceuta/Melilla** choices. Sark, Diego Garcia and Clipperton have source-backed reference features (Clipperton retains both its unspecified administrative and atoll records); those features do **not** establish a complete island-membership crosswalk or containment polygon. Their manifest gaps remain explicit. A canonical-country fallback must not silently make these exceptional contexts equivalent to the whole parent country.

## Deliberate remaining limits

GeoNames is a useful worldwide reference, not an exhaustive current rural settlement or street/postcode directory. Counts do not establish worldwide listing readiness. Source histories, cross-border features, missing timezones, ambiguous parents and special-context membership need review where relevant to actual listing rules. `manifest.json` preserves those counts and gaps. Postal formats/subdivision rules, phone metadata, country policy activation, national licensing/legal acceptance and live geocoding-provider configuration are separate concerns. This snapshot adds no tracking, outbound messages, production ingestion schedule or automatic activation.
