# ZA — South Africa geography review draft

Country register · Geography specification

State: **research draft; full data/lookup/UX acceptance not completed**. Code ZA; English display South Africa. Do not confuse SA with South Africa: country-code aliases require explicit handling.

## Administrative and browse rules

Country → province → useful city/town/locality/suburb for browsing. Administrative tags retain the actual metro or district/local-municipality relationships. A metro is not forced into a fictional district/local pair. Municipal membership is not inferred from a matching place-name string.

The [South African Government](https://www.gov.za/about-sa/south-africas-provinces) identifies nine provinces: Eastern Cape, Free State, Gauteng, KwaZulu-Natal, Limpopo, Mpumalanga, North West, Northern Cape and Western Cape. Use stable source identifiers and approved aliases rather than slugs as identity. The [local government reference](https://www.gov.za/about-government/government-system/local-government) distinguishes municipal structures. Do not freeze a municipal count from an old page as a timeless rule.

## Address and display draft

Use Province for geographic browse/membership and Postal code for the address field. The inspected ZA postal template uses address lines → dependent locality/suburb → locality → postcode and omits province; do not inject a mandatory postal province. Support building/unit/address lines and preserve supplied spelling. Postal codes are strings so leading zeros survive. A street/public premises address differs from a PO box/postal address. Service-area/home-based businesses may withhold the street and show coverage; do not require a public residential address to get a profile.

Default phone assistance can use +27 but must accept a business's valid international numbers and extensions. Currency suggestions may use ZAR; do not assume every price is ZAR without explicit currency. Branch hours use an explicitly selected IANA timezone, not a numerical offset copied globally.

## Source crosswalk checked 25 October 2026

The pinned library has a dedicated ZA address format but **no ZA subdivision root**. Its generic Province label is not province data. GeoNames supplies the nine province records below; names agree with the cited government list. These source keys/IDs are not ISO or Stats SA codes. Keep their namespace/version and map them to internal province IDs when importing is authorised.

| Province | GeoNames ADM1 key | GeoNames ID |
| --- | --- | --- |
| Eastern Cape | ZA.05 | 1085593 |
| Free State | ZA.03 | 967573 |
| Gauteng | ZA.06 | 1085594 |
| KwaZulu-Natal | ZA.02 | 972062 |
| Limpopo | ZA.09 | 1085597 |
| Mpumalanga | ZA.07 | 1085595 |
| Northern Cape | ZA.08 | 1085596 |
| North West | ZA.10 | 1085598 |
| Western Cape | ZA.11 | 1085599 |

Reference: [GeoNames ADM1 source](https://download.geonames.org/export/dump/admin1CodesASCII.txt), dated/hash-pinned in [the source evidence](source-evidence.md). No live place import or municipality boundary test occurred. Do not map the numeric suffixes directly to another provider's province codes. Source ADM2 includes metro/district-level areas; the actual municipal type comes from reviewed national data, not the ADM2 label.

Working form: country/territory → useful locality with province context → country-aware street lookup and optional address details → owner-confirmed pin/visibility. Province is selectable to disambiguate or confirm an uncertain locality; municipality tiers need not become compulsory owner questions. A Cape Town metro case must not acquire a fictional district/local pair. Branch timezone candidate is Africa/Johannesburg; validate the actual selected location and deployed IANA data.

## Required evidence before ready

Confirm metadata/format rules from the pinned source, review province and selected locality/municipal data, verify representative metro/non-metro/rural/postal cases, exercise actual provider lookup and private-pin handling, check aliases and missing-place correction, and record reviewer/version/outcome. This document does not establish completed implementation or data import.
