# Country mapping source evidence

Workbench · [Matrix](mapping-matrix.md) · [Contract](mapping-contract.md)

Read-only source audit on **25 October 2026**. Downloaded research inputs to a temporary research directory outside the repository; this project still contains only Markdown. No packages installed, application/import executed, external account created or keyed geocoding request made.

## Versions and reproducibility

CommerceGuys Addressing commit `e3ce66714cfa181b848533d926e8583261253c9e`; Unicode CLDR 49 release commit `96e54b273d2da4ec6fbad350ba19ff23fa24a588`; IANA tzdb source version **2026e**. GeoNames and UPU are dated fetches, not immutable upstream versions. Pin approved import snapshots/digests when implementation is authorised; do not rely on a moving download URL to reproduce a release.

| Input | Reference | SHA-256 of inspected content |
| --- | --- | --- |
| countries.json | [source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/resources/country/en.json) | `7e23d20fd8a03abf22816bd557317f0dc60b772dc741f97d3f1c44a0d712f0b1` |
| formats.php | [source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/src/AddressFormat/AddressFormatRepository.php) | `7ee753aac551f19453a225e43fc059d098945351d2e8409a61950f8aeb501d77` |
| country_repo.php | [source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/src/Country/CountryRepository.php) | `66a0351f38595a6e1a3631c8833164c2eed73e7aeaac74dfabf047dda8c2a600` |
| cldr_validity.xml | [source](https://raw.githubusercontent.com/unicode-org/cldr/96e54b273d2da4ec6fbad350ba19ff23fa24a588/common/validity/region.xml) | `e751e0eedd46b52c38f3cdb72b0fab61ac8b48e052e8b28ba74b6ac26c4c8cb1` |
| cldr_aliases.xml | [source](https://raw.githubusercontent.com/unicode-org/cldr/96e54b273d2da4ec6fbad350ba19ff23fa24a588/common/supplemental/supplementalMetadata.xml) | `b06614fc2c9aab3b9a9f7e8bf9328f4f7a95d89b2d2dbb300d0caff0f885c164` |
| geonames_country.txt | [source](https://download.geonames.org/export/dump/countryInfo.txt) | `c55f638cfaafb4fe45a9aa15120a0f1f78e8a34a8e1847d7b9320cf740fbc9ab` |
| geonames_admin1.txt | [source](https://download.geonames.org/export/dump/admin1CodesASCII.txt) | `2e4867f5397acb056ea26377601b57af37cb4c81399770225018e9e439e91ad3` |
| geonames_admin2.txt | [source](https://download.geonames.org/export/dump/admin2Codes.txt) | `9f49795da1fd460006a40e58a614dbc1a351c9277340a65fe8d73b5f97ec1852` |
| iana_zone.tab | [source](https://data.iana.org/time-zones/tzdb/zone.tab) | `e2e8e31c4e10f44576c79345e76060591dbb3eef6ce14e006afc8a373caa9593` |
| cldr_en.xml | [source](https://raw.githubusercontent.com/unicode-org/cldr/96e54b273d2da4ec6fbad350ba19ff23fa24a588/common/main/en.xml) | `f8cbf26964d0e349fc96d9e5a56292edcbaab25c8e64177ca4f111773dfb79cf` |

The pinned repository tree and all **63** root subdivision JSON files were inspected. The matrix shows root choice counts and declared field roles, not a full subdivision/boundary import. Address fields/requiredness were read from country definitions with documented generic inheritance; no fetched PHP source was executed. Recipient-name injection was deliberately kept out of directory requirements. All extracted required fields were present in their source formats.

## Results across the whole inventory

- Original country catalogue: 256 entries. Pinned CLDR 49 has 257 regular region identifiers; **CQ (Sark)** is the one missing entry. CLDR regular-region status does not mean ordinary ISO assignment or sovereign-country status.
- Three English display labels differ: HM becomes Heard Island & McDonald Islands; SH becomes St. Helena, Ascension & Tristan da Cunha; TF becomes French Southern and Antarctic Lands. Keep previous wording as searchable aliases. This is a label update, not a boundary change.
- 206 dedicated address definitions; **51** missing dedicated definitions after adding CQ. Of those, 50 use the existing library fallback; CQ is also absent from its country repository and needs a reviewed overlay before use.
- 63 subdivision root files, all tied to declared subdivision-data fields; 194 candidates lack such a file. README's advertised 62-country count is not the inspected file count.
- GeoNames country file: 252 rows, including obsolete AN/CS. Current inventory matches 250; AC/CP/CQ/DG/EA/IC/TA lack country rows. Do not import obsolete entries as current countries.
- GeoNames administrative files: 3,865 ADM1 and 47,764 ADM2 rows. All ADM2 parent keys were found in ADM1. This checks structure, not administrative currency or locality completeness. Most ADM1 keys are FIPS/mixed identifiers, as the publisher documents.
- IANA zone.tab lacks a country row for AC/BV/CP/CQ/DG/EA/HM/IC/TA/XK. Shared/exceptional locations need explicit mapping; no-row does not mean UTC. Runtime PHP timezone data must support the approved zone IDs/aliases; a source file alone does not establish runtime compatibility.
- UPU country-sheet selector: **224** supplied document links; **224** returned successful PDF content. The initial selector join associated 228 inventory entries with a document. Follow-on content checks found misleading groupings and verified direct replacement/additional sheets; the current matrix has 232 document associations, including two remaining unconfirmed selector groupings (BL/MF). PDF link checks alone do not validate document contents, dates or global correctness.

## Sources, rights and unresolved evidence

[UPU addressing systems and selector](https://www.upu.int/en/Postal-Solutions/Programmes-Services/Addressing-Solutions) supplies the document links; the linked sheets may be dated and are references, not permission to redistribute a postal-address database. Selector group labels include Aruba/Curaçao/Sint Maarten, Guadeloupe/St Barthélemy/St Martin and French Polynesia/Clipperton. These labels cannot establish actual PDF coverage or administrative parentage. The [fallback review](fallback-address-review.md) found misleading AW/PF associations, verified direct replacements and read 46 country references, with dated findings and anomalies. At least 12 fallback countries need postcode fields missing from the library generic form; five lack a standalone UPU sheet; CQ/EA/IC have separate parent-format routes backed by postal-operator/national code sources. All 51 remain subject to country QA.

[GeoNames documentation](https://download.geonames.org/export/dump/readme.txt) explains levels/codes and its CC BY 4.0 attribution/no-completeness terms. [CLDR release/code documentation](https://unicode.org/reports/tr35/tr35.html) explains region semantics and aliases; retain its [Unicode licence](https://www.unicode.org/license.txt) for adopted data. [IANA tzdb](https://www.iana.org/time-zones) describes timezone data. CommerceGuys MIT notices remain in source notices. Counts/transformed references here are research findings, not a merged production database or data-resale licence.

National examples and current-authority differences are cited in [mapping exceptions](mapping-exceptions.md), ZA and GB. Every other country's current administrative meanings/localities, applicable postal examples, geocoder component mappings, location/zone/private-address behaviour and provider/source rights remain country-specific release evidence. The register deliberately marks M/P/S/Z audit progress separately from passed acceptance. No country has been declared ready from a library/file count.
