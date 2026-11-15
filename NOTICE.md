# Third-party sources

This repository contains pinned copies of, and data derived from, the sources
below. Each keeps its own licence. Exact versions, URLs, byte counts and
SHA-256 digests are in the manifest next to each source.

| Source | Version | Used for | Licence | Files |
| --- | --- | --- | --- | --- |
| Unicode CLDR | 49 | Region validity, territory crosswalks, deprecated aliases, English names | Unicode License V3 | `resources/data/country-sources/` (`Unicode-LICENSE.txt`) |
| IANA Time Zone Database | 2026e | Country to timezone associations | Public domain | `resources/data/country-sources/` (`IANA-LICENSE.txt`) |
| CommerceGuys Addressing | commit e3ce667 | Address formats and subdivision lists | MIT | `resources/data/addressing/` (`commerceguys-LICENSE`) |
| Google libaddressinput | pinned reference, see `google-source-ref.json` | Address metadata cross-check | Apache 2.0 | `resources/data/addressing/` (`google-libaddressinput-LICENSE`) |
| Google libphonenumber | v9.0.42 | Telephone numbering plan metadata | Apache 2.0 | `resources/data/phone-metadata/` (`LICENSE`) |
| GeoNames | snapshot of 27 October 2026 | Administrative and populated-place counts and roots | CC BY 4.0 | `resources/data/geonames/` |

Attribution required by GeoNames: GeoNames, https://www.geonames.org/

Postal examples marked as separately attributed in `postal-evidence.v1.json`
cite their own source for each entry.

None of these sources certifies current national address rules, boundaries or
telephone assignments, and neither does this repository.
