# Pinned country identity sources

This catalog supplies identity and source-associated timezone metadata. It does not supply or approve national address, postcode, telephone, administrative-boundary, provider, political/jurisdiction, tax or publication rules.

- **Unicode CLDR49:** region validity, territory code crosswalks and deprecated aliases are pinned to official unicode-org/cldr commit `96e54b273d2da4ec6fbad350ba19ff23fa24a588`. English display names use the official unicode-org/cldr-json49.0.0 release. Exact URLs, byte counts and SHA256 digests are in `manifest.v1.json`. The copied Unicode License V3 is in `Unicode-LICENSE.txt`.
- **IANA tzdb2026e:** the official release archive supplies `iso3166.tab`, `zone.tab`, `zone1970.tab`, Zone/Link identities and license/version. Its `iso3166.tab` header identifies an ISO/TC46 N1127 snapshot dated2024-02-29; it is **not a newly downloaded live ISO export**. The official ISO public page returned403 during this review. ISO alpha3/numeric facts are taken from CLDR's maintained ISO crosswalk for only the249 codes in that IANA ISO inventory. Independent current ISO confirmation remains a separate source-review input. The IANA data/license copied here are public domain, as specified in `IANA-LICENSE.txt` and the archive.

`country-catalog.v1.json` contains249 ISO-assigned countries plus the explicit non-ISO XK record, and257 supported CLDR regular selectors. XA/XB pseudolocales, macroregions and ZZ are excluded. XK has no ISO alpha3 or numeric fields: CLDR's XKK/983 must never be described as ISO assignments. CQ/Sark remains a CLDR selector mapped to GG, not an assigned ISO country. UK is an explicit alias for GB; historical codes such as AN/CS/SU/YU require a new explicit selection rather than guessing a successor.

The six additional territory records are AC→SH, CP→FR, CQ→GG, DG→IO, IC→ES and TA→SH. EA→ES is a combined Ceuta/Melilla place choice, not one generic territory. The catalog does not invent geographic place IDs or an approved place-choice mapping. Existing wrong EA context metadata is reconciled without deleting historical IDs.

The catalog contains598 IANA Zone/Link names and841 `(country, timezone, source table)` associations. `zone1970.tab` lists multiple countries on one comma-separated row; the builder preserves every explicit association. It is not interchangeable with `zone.tab`. AC, BV, CP, CQ, DG, EA, HM, IC, TA and XK have no direct `zone.tab` row. A special selector must not inherit a parent country's timezone or default to UTC. Runtime PHP recognition is reported separately from IANA inventory, and neither means the application's context timezone policy has been reviewed.

## Reproduce and review updates

Run from the repository root, without a network or database:

```sh
python3 resources/data/country-sources/build.py --check
```

This verifies every pinned input hash and deterministically compares the derived JSON and its SHA256 sidecar. Running the same builder without `--check` rebuilds only those two identity metadata files. The builder reads explicit tar members and never extracts or executes archive code.

To update, select reviewed official Unicode/IANA release identifiers, download the exact manifest URLs into this directory, inspect the changes and licenses, and update the version, URLs and input digests deliberately. Do not silently replace the bytes under an existing catalog version. Run the builder and pure country tests; changes in ISO/selector membership fail closed for explicit code/schema review. Before database backfill, rehearse on isolated data and inspect stable IDs, changed display names, historical aliases and all special selectors. No approved context, provider policy or activation is changed by a metadata update.

Migration76 adds nullable paired ISO codes and a separate unreviewed timezone inventory. `seed_country_catalog()` transactionally reconciles identity metadata even when synthetic fixtures already exist. Existing primary IDs, current graph/rule pointers, activation/review states, approved context timezone choices and provider policies remain separate. A conflicting existing selector/canonical-country relation or reused source version with different bytes requires explicit review; the seed does not silently move it. Catalog version/source rows are retained as provenance. Database seeding does not download external data.
