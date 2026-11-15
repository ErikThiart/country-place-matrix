# All-country source mapping matrix

Workbench · [Contract](mapping-contract.md) · [Cases](mapping-exceptions.md) · [Evidence](source-evidence.md)

Checked 25 October 2026: **257 distinct candidates**, 206 dedicated address definitions, 51 missing dedicated definitions; 63 library subdivision roots. Original country labels were cross-checked against pinned CLDR 49; CQ was added and HM/SH/TF display labels updated, with old labels retained as aliases.

This is a source-to-product mapping worksheet, not completed national boundary QA or a working address lookup. Ordinary codes retain their context; exceptional selectors show the proposed canonical country plus territory/place. Parent mappings marked review need current authority confirmation.

Postal roles shown in source-template order: **A** administrative address area, **L** postal locality, **D** dependent locality, **P** postcode, **S** sorting code. `*` means required by the upstream postal definition before recipient-name injection; `~` means its label is inherited from the library generic default. Address lines/recipient/organisation are omitted for readability; upstream requires addressLine1 in every definition, and injects given/family names in processing. These are **not** universal directory requirements. Native-script order, original text and directory-purpose overlays remain mandatory.

Postal seeds count **root choices**, with their source field roles; they are neither current official admin counts nor total child counts. GeoNames A1/A2 are separate source levels with FIPS/mixed keys. IANA column counts zone.tab references, not allowed global membership or coordinate boundaries. `—` means the relevant source lacks an entry, not that the real country lacks regions, postcodes or a timezone.

UPU selector links were checked as successful PDFs. Follow-on content review found misleading selector groupings; verified direct CW/SX/CP sheets replace them, with additional direct BV/NU/PS/TK references. Remaining `selector grouping` labels record the selector association only, without asserting document coverage. See the [51-country fallback review](fallback-address-review.md) for dated postal findings, required corrections and anomalies. No unavailable HTML response is treated as a PDF.

| Code / country or territory | Canonical context | Source postal roles | Postal seeds (root) | GeoNames A1 / A2 | IANA refs | Evidence / exception |
| --- | --- | --- | --- | --- | --- | --- |
| AC — Ascension Island | SH + AC | L:city~* → P:postcode~ | — | — | — | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ascEn.pdf); [special code](mapping-exceptions.md#special-territory-selectors--working-canonical-treatment) |
| AD — Andorra | AD | P:postcode~ → L:city~* | L=7 | 7 / 0 | `Europe/Andorra` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/andEn.pdf) |
| AE — United Arab Emirates | AE | L:city~ → A:emirate* | A=7 | 7 / 28 | `Asia/Dubai` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/areEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| AF — Afghanistan | AF | L:city~* → P:postcode~ | — | 34 / 398 | `Asia/Kabul` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/afgEn.pdf) |
| AG — Antigua & Barbuda | AG | L:city~ | — | 8 / 0 | `America/Antigua` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/atgEn.pdf) |
| AI — Anguilla | AI | L:city~* → P:postcode~ | — | 14 / 0 | `America/Anguilla` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/aiaEn.pdf) |
| AL — Albania | AL | P:postcode~ → L:city~* | — | 12 / 61 | `Europe/Tirane` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/albEn.pdf) |
| AM — Armenia | AM | P:postcode~ → L:city~* → A:province~ | A=11 | 11 / 82 | `Asia/Yerevan` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/armEn.pdf) |
| AO — Angola | AO | **Fallback:** L:city~* | — | 21 / 162 | `Africa/Luanda` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/agoEn.pdf); [postal review](fallback-address-review.md) |
| AQ — Antarctica | AQ | **Fallback:** L:city~* | — | 0 / 0 | 10 refs | UPU match pending |
| AR — Argentina | AR | P:postcode~ → L:city~* → A:province~ | A=24 | 24 / 529 | 12 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/argEn.pdf) |
| AS — American Samoa | AS | L:city~* → P:ZIP* | — | 5 / 14 | `Pacific/Pago_Pago` | UPU match pending |
| AT — Austria | AT | P:postcode~* → L:city~* | — | 9 / 94 | `Europe/Vienna` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/autEn.pdf) |
| AU — Australia | AU | L:suburb* → A:state* → P:postcode~* | A=8 | 8 / 540 | 12 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ausEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| AW — Aruba | AW | **Fallback:** L:city~* | — | 0 / 0 | `America/Aruba` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/abwEn.pdf); [postal review](fallback-address-review.md) |
| AX — Åland Islands | AX | P:postcode~* → L:city~* | — | 3 / 16 | `Europe/Mariehamn` | UPU match pending |
| AZ — Azerbaijan | AZ | P:postcode~ → L:city~* | — | 71 / 21 | `Asia/Baku` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/azeEn.pdf) |
| BA — Bosnia & Herzegovina | BA | P:postcode~ → L:city~* | — | 3 / 18 | `Europe/Sarajevo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bihEn.pdf) |
| BB — Barbados | BB | L:city~* → A:parish* → P:postcode~ | A=11 | 11 / 0 | `America/Barbados` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/brbEn.pdf) |
| BD — Bangladesh | BD | L:city~* → P:postcode~ | — | 8 / 64 | `Asia/Dhaka` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bgdEn.pdf) |
| BE — Belgium | BE | P:postcode~* → L:city~* | — | 3 / 11 | `Europe/Brussels` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/belEn.pdf) |
| BF — Burkina Faso | BF | L:city~* → S:sorting | — | 13 / 45 | `Africa/Ouagadougou` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bfaEn.pdf) |
| BG — Bulgaria | BG | P:postcode~ → L:city~* | — | 28 / 265 | `Europe/Sofia` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bgrEn.pdf) |
| BH — Bahrain | BH | L:city~* → P:postcode~ | — | 4 / 0 | `Asia/Bahrain` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bhrEn.pdf) |
| BI — Burundi | BI | **Fallback:** L:city~* | — | 16 / 119 | `Africa/Bujumbura` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bdiEn.pdf); [postal review](fallback-address-review.md) |
| BJ — Benin | BJ | L:city~* | — | 12 / 77 | `Africa/Porto-Novo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/benEn.pdf) |
| BL — St. Barthélemy | BL | P:postcode~* → L:city~* | — | 0 / 0 | `America/St_Barthelemy` | [UPU selector grouping](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/glpEn.pdf) |
| BM — Bermuda | BM | L:city~* → P:postcode~ | — | 11 / 0 | `Atlantic/Bermuda` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bmuEn.pdf) |
| BN — Brunei | BN | L:city~* → P:postcode~ | — | 4 / 40 | `Asia/Brunei` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/brnEn.pdf) |
| BO — Bolivia | BO | L:city~* | — | 9 / 112 | `America/La_Paz` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bolEn.pdf) |
| BQ — Caribbean Netherlands | BQ | **Fallback:** L:city~* | — | 3 / 0 | `America/Kralendijk` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/besEn.pdf); [postal review](fallback-address-review.md) |
| BR — Brazil | BR | D:neighborhood → L:city~* → A:state* → P:postcode~* | A/L=27 | 27 / 5570 | 16 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/braEn.pdf) |
| BS — Bahamas | BS | L:city~* → A:island | A=32 | 32 / 0 | `America/Nassau` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bhsEn.pdf) |
| BT — Bhutan | BT | L:city~* → P:postcode~ | — | 20 / 27 | `Asia/Thimphu` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/btnEn.pdf) |
| BV — Bouvet Island | BV | **Fallback:** L:city~* | — | 0 / 0 | — | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bvtEn.pdf); [postal review](fallback-address-review.md) |
| BW — Botswana | BW | **Fallback:** L:city~* | — | 16 / 25 | `Africa/Gaborone` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bwaEn.pdf); [postal review](fallback-address-review.md) |
| BY — Belarus | BY | P:postcode~ → L:city~* → A:region | — | 7 / 158 | `Europe/Minsk` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/blrEn.pdf) |
| BZ — Belize | BZ | **Fallback:** L:city~* | — | 6 / 2 | `America/Belize` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/blzEn.pdf); [postal review](fallback-address-review.md) |
| CA — Canada | CA | L:city~* → A:province~* → P:postcode~* | A=13 | 13 / 1641 | 23 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/canEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| CC — Cocos (Keeling) Islands | CC | L:city~* → P:postcode~ | — | 0 / 0 | `Indian/Cocos` | UPU match pending |
| CD — Congo - Kinshasa | CD | **Fallback:** L:city~* | — | 26 / 195 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/codEn.pdf); [postal review](fallback-address-review.md) |
| CF — Central African Republic | CF | **Fallback:** L:city~* | — | 20 / 71 | `Africa/Bangui` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cafEn.pdf); [postal review](fallback-address-review.md) |
| CG — Congo - Brazzaville | CG | **Fallback:** L:city~* | — | 12 / 89 | `Africa/Brazzaville` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cogEn.pdf); [postal review](fallback-address-review.md) |
| CH — Switzerland | CH | P:postcode~* → L:city~* | — | 26 / 149 | `Europe/Zurich` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cheEn.pdf) |
| CI — Côte d’Ivoire | CI | S:sorting → L:city~* → S:sorting | — | 14 / 33 | `Africa/Abidjan` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/civEn.pdf) |
| CK — Cook Islands | CK | **Fallback:** L:city~* | — | 11 / 8 | `Pacific/Rarotonga` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cokEn.pdf); [postal review](fallback-address-review.md) |
| CL — Chile | CL | P:postcode~ → L:city~* → A:region* | A/L=16 | 16 / 56 | 4 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/chlEn.pdf) |
| CM — Cameroon | CM | **Fallback:** L:city~* | — | 10 / 58 | `Africa/Douala` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cmrEn.pdf); [postal review](fallback-address-review.md) |
| CN — China | CN | D:district → L:city~* → A:province~* → P:postcode~* | A/L/D=34 | 31 / 360 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/chnEn.pdf) |
| CO — Colombia | CO | L:city~* → A:department* → P:postcode~ | A=33 | 33 / 1122 | `America/Bogota` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/colEn.pdf) |
| CP — Clipperton Island | FR + CP (review) | **Fallback:** L:city~* | — | — | — | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cptEn.pdf); [special code](mapping-exceptions.md#special-territory-selectors--working-canonical-treatment); [postal review](fallback-address-review.md) |
| CQ — Sark | GG + CQ | **Fallback:** L:city~* | — | — | — | [parent-format evidence](mapping-exceptions.md#explicit-parent-format-crosswalks); [special code](mapping-exceptions.md#special-territory-selectors--working-canonical-treatment) |
| CR — Costa Rica | CR | A:province~* → L:city~* → P:postcode~ | A=7 | 7 / 82 | `America/Costa_Rica` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/criEn.pdf) |
| CU — Cuba | CU | L:city~* → A:province~ → P:postcode~ | A=16 | 16 / 167 | `America/Havana` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cubEn.pdf) |
| CV — Cape Verde | CV | P:postcode~ → L:city~* → A:island* | A=9 | 22 / 32 | `Atlantic/Cape_Verde` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cpvEn.pdf) |
| CW — Curaçao | CW | **Fallback:** L:city~* | — | 0 / 0 | `America/Curacao` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cuwEn.pdf); [postal review](fallback-address-review.md) |
| CX — Christmas Island | CX | L:city~* → P:postcode~ | — | 0 / 0 | `Indian/Christmas` | UPU match pending |
| CY — Cyprus | CY | P:postcode~ → L:city~* | — | 6 / 615 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cypEn.pdf) |
| CZ — Czechia | CZ | P:postcode~* → L:city~* | — | 14 / 98 | `Europe/Prague` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/czeEn.pdf) |
| DE — Germany | DE | P:postcode~* → L:city~* | — | 16 / 20 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/deuEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| DG — Diego Garcia | IO + DG (review) | **Fallback:** L:city~* | — | — | — | UPU match pending; [special code](mapping-exceptions.md#special-territory-selectors--working-canonical-treatment) |
| DJ — Djibouti | DJ | **Fallback:** L:city~* | — | 6 / 3 | `Africa/Djibouti` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/djiEn.pdf); [postal review](fallback-address-review.md) |
| DK — Denmark | DK | P:postcode~* → L:city~* | — | 5 / 99 | `Europe/Copenhagen` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/dnkEn.pdf) |
| DM — Dominica | DM | **Fallback:** L:city~* | — | 10 / 0 | `America/Dominica` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/dmaEn.pdf); [postal review](fallback-address-review.md) |
| DO — Dominican Republic | DO | P:postcode~ → L:city~* | — | 32 / 155 | `America/Santo_Domingo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/domEn.pdf) |
| DZ — Algeria | DZ | P:postcode~ → L:city~* | — | 58 / 548 | `Africa/Algiers` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/dzaEn.pdf) |
| EA — Ceuta & Melilla | ES + selected place | **Fallback:** L:city~* | — | — | — | [parent-format evidence](mapping-exceptions.md#explicit-parent-format-crosswalks); [special code](mapping-exceptions.md#special-territory-selectors--working-canonical-treatment) |
| EC — Ecuador | EC | P:postcode~ → L:city~* | — | 24 / 221 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ecuEn.pdf) |
| EE — Estonia | EE | P:postcode~* → L:city~* → A:county | A=15 | 15 / 79 | `Europe/Tallinn` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/estEn.pdf) |
| EG — Egypt | EG | L:city~* → A:province~* → P:postcode~ | A=27 | 27 / 138 | `Africa/Cairo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/egyEn.pdf) |
| EH — Western Sahara | EH | P:postcode~ → L:city~* | — | 0 / 0 | `Africa/El_Aaiun` | UPU match pending |
| ER — Eritrea | ER | **Fallback:** L:city~* | — | 6 / 58 | `Africa/Asmara` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/eriEn.pdf); [postal review](fallback-address-review.md) |
| ES — Spain | ES | P:postcode~* → L:city~* → A:province~* | A=52 | 19 / 52 | 3 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/espEn.pdf) |
| ET — Ethiopia | ET | P:postcode~ → L:city~* | — | 14 / 123 | `Africa/Addis_Ababa` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ethEn.pdf) |
| FI — Finland | FI | P:postcode~* → L:city~* | — | 18 / 66 | `Europe/Helsinki` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/finEn.pdf) |
| FJ — Fiji | FJ | **Fallback:** L:city~* | — | 5 / 15 | `Pacific/Fiji` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/fjiEn.pdf); [postal review](fallback-address-review.md) |
| FK — Falkland Islands | FK | L:city~* → P:postcode~* | — | 0 / 0 | `Atlantic/Stanley` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/flkEn.pdf) |
| FM — Micronesia | FM | L:city~* → A:state* → P:ZIP* | A=4 | 4 / 78 | 3 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/fsmEn.pdf) |
| FO — Faroe Islands | FO | P:postcode~ → L:city~* | — | 6 / 29 | `Atlantic/Faroe` | UPU match pending |
| FR — France | FR | P:postcode~* → L:city~* → S:sorting | — | 13 / 96 | `Europe/Paris` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/fraEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| GA — Gabon | GA | **Fallback:** L:city~* | — | 9 / 48 | `Africa/Libreville` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gabEn.pdf); [postal review](fallback-address-review.md) |
| GB — United Kingdom | GB | L:town/city* → A:county → P:postcode~* | A=217 | 4 / 185 | `Europe/London` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gbrEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| GD — Grenada | GD | **Fallback:** L:city~* | — | 7 / 0 | `America/Grenada` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/grdEn.pdf); [postal review](fallback-address-review.md) |
| GE — Georgia | GE | P:postcode~ → L:city~* | — | 12 / 84 | `Asia/Tbilisi` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/geoEn.pdf) |
| GF — French Guiana | GF | P:postcode~* → L:city~* | — | 1 / 1 | `America/Cayenne` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gufEn.pdf) |
| GG — Guernsey | GG | L:city~* → P:postcode~* | — | 11 / 0 | `Europe/Guernsey` | UPU match pending |
| GH — Ghana | GH | **Fallback:** L:city~* | — | 16 / 265 | `Africa/Accra` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ghaEn.pdf); [postal review](fallback-address-review.md) |
| GI — Gibraltar | GI | P:postcode~ | — | 0 / 0 | `Europe/Gibraltar` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gibEn.pdf) |
| GL — Greenland | GL | P:postcode~* → L:city~* | — | 5 / 3 | 4 refs | UPU match pending |
| GM — Gambia | GM | **Fallback:** L:city~* | — | 6 / 37 | `Africa/Banjul` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gmbEn.pdf); [postal review](fallback-address-review.md) |
| GN — Guinea | GN | P:postcode~ → L:city~* | — | 8 / 34 | `Africa/Conakry` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ginEn.pdf) |
| GP — Guadeloupe | GP | P:postcode~* → L:city~* | — | 1 / 1 | `America/Guadeloupe` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/glpEn.pdf) |
| GQ — Equatorial Guinea | GQ | **Fallback:** L:city~* | — | 8 / 32 | `Africa/Malabo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gnqEn.pdf); [postal review](fallback-address-review.md) |
| GR — Greece | GR | P:postcode~* → L:city~* | — | 14 / 54 | `Europe/Athens` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/grcEn.pdf) |
| GS — South Georgia & South Sandwich Islands | GS | L:city~* → P:postcode~* | — | 0 / 0 | `Atlantic/South_Georgia` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sgsEn.pdf) |
| GT — Guatemala | GT | P:postcode~ → L:city~* → A:department | A=22 | 22 / 340 | `America/Guatemala` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gtmEn.pdf) |
| GU — Guam | GU | L:city~* → P:ZIP* | — | 19 / 0 | `Pacific/Guam` | UPU match pending |
| GW — Guinea-Bissau | GW | P:postcode~ → L:city~* | — | 9 / 39 | `Africa/Bissau` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gnbEn.pdf) |
| GY — Guyana | GY | **Fallback:** L:city~* | — | 10 / 0 | `America/Guyana` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/guyEn.pdf); [postal review](fallback-address-review.md) |
| HK — Hong Kong SAR China | HK | L:district → A:area* | A/L=3 | 18 / 0 | `Asia/Hong_Kong` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/hkgEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| HM — Heard Island & McDonald Islands | HM | L:city~* → P:postcode~ | — | 0 / 0 | — | UPU match pending |
| HN — Honduras | HN | L:city~* → A:department* → P:postcode~ | A=18 | 18 / 298 | `America/Tegucigalpa` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/hndEn.pdf) |
| HR — Croatia | HR | P:postcode~ → L:city~* | — | 21 / 572 | `Europe/Zagreb` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/hrvEn.pdf) |
| HT — Haiti | HT | P:postcode~ → L:city~* | — | 10 / 42 | `America/Port-au-Prince` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/htiEn.pdf) |
| HU — Hungary | HU | L:city~* → P:postcode~* | — | 20 / 197 | `Europe/Budapest` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/hunEn.pdf) |
| IC — Canary Islands | ES + IC | **Fallback:** L:city~* | — | — | — | [parent-format evidence](mapping-exceptions.md#explicit-parent-format-crosswalks); [special code](mapping-exceptions.md#special-territory-selectors--working-canonical-treatment) |
| ID — Indonesia | ID | L:city~ → A:province~* → P:postcode~ | A=38 | 38 / 514 | 4 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/idnEn.pdf) |
| IE — Ireland | IE | D:townland → L:city~* → A:county → P:Eircode | A=26 | 4 / 31 | `Europe/Dublin` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/irlEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| IL — Israel | IL | L:city~* → P:postcode~ | — | 7 / 17 | `Asia/Jerusalem` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/isrEn.pdf) |
| IM — Isle of Man | IM | L:city~* → P:postcode~* | — | 24 / 0 | `Europe/Isle_of_Man` | UPU match pending |
| IN — India | IN | L:city~* → P:PIN* → A:state* | A=36 | 36 / 763 | `Asia/Kolkata` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/indEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| IO — British Indian Ocean Territory | IO | L:city~* → P:postcode~* | — | 0 / 0 | `Indian/Chagos` | UPU match pending |
| IQ — Iraq | IQ | L:city~* → A:province~* → P:postcode~ | — | 19 / 122 | `Asia/Baghdad` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/irqEn.pdf) |
| IR — Iran | IR | A:province~* → L:city~* → D:neighborhood → P:postcode~ | A=31 | 31 / 433 | `Asia/Tehran` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/irnEn.pdf) |
| IS — Iceland | IS | P:postcode~ → L:city~* | — | 8 / 64 | `Atlantic/Reykjavik` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/islEn.pdf) |
| IT — Italy | IT | P:postcode~* → L:city~* → A:province~* | A=110 | 20 / 107 | `Europe/Rome` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/itaEn.pdf) |
| JE — Jersey | JE | L:city~* → P:postcode~* | — | 12 / 0 | `Europe/Jersey` | UPU match pending |
| JM — Jamaica | JM | L:city~* → A:parish* → S:sorting | A=14 | 14 / 825 | `America/Jamaica` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/jamEn.pdf) |
| JO — Jordan | JO | L:city~* → P:postcode~ | — | 12 / 53 | `Asia/Amman` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/jorEn.pdf) |
| JP — Japan | JP | L:city~ → A:prefecture* → P:postcode~* | A=47 | 47 / 1190 | `Asia/Tokyo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/jpnEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| KE — Kenya | KE | L:city~* → P:postcode~ | — | 47 / 32 | `Africa/Nairobi` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/kenEn.pdf) |
| KG — Kyrgyzstan | KG | P:postcode~ → L:city~* | — | 9 / 45 | `Asia/Bishkek` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/kgzEn.pdf) |
| KH — Cambodia | KH | L:city~* → P:postcode~ | — | 25 / 199 | `Asia/Phnom_Penh` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/khmEn.pdf) |
| KI — Kiribati | KI | A:island* → L:city~* | A=3 | 3 / 33 | 3 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/kirEn.pdf) |
| KM — Comoros | KM | L:city~* | — | 3 / 0 | `Indian/Comoro` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/comEn.pdf) |
| KN — St. Kitts & Nevis | KN | L:city~* → A:island* | A=2 | 14 / 0 | `America/St_Kitts` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/knaEn.pdf) |
| KP — North Korea | KP | L:city~* → A:province~ → P:postcode~ | A=11 | 13 / 201 | `Asia/Pyongyang` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/prkEn.pdf) |
| KR — South Korea | KR | D:district → L:city~* → A:do/si* → P:postcode~* | A/L/D=17 | 17 / 229 | `Asia/Seoul` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/korEn.pdf) |
| KW — Kuwait | KW | P:postcode~ → L:city~* | — | 6 / 109 | `Asia/Kuwait` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/kwtEn.pdf) |
| KY — Cayman Islands | KY | A:island* → P:postcode~ | A=3 | 6 / 0 | `America/Cayman` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cymEn.pdf) |
| KZ — Kazakhstan | KZ | P:postcode~* → L:city~* → A:region | A=20 | 21 / 279 | 7 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/kazEn.pdf) |
| LA — Laos | LA | P:postcode~ → L:city~* | — | 18 / 148 | `Asia/Vientiane` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/laoEn.pdf) |
| LB — Lebanon | LB | L:city~* → P:postcode~ | — | 8 / 30 | `Asia/Beirut` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lbnEn.pdf) |
| LC — St. Lucia | LC | **Fallback:** L:city~* | — | 10 / 546 | `America/St_Lucia` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lcaEn.pdf); [postal review](fallback-address-review.md) |
| LI — Liechtenstein | LI | P:postcode~* → L:city~* | — | 11 / 0 | `Europe/Vaduz` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lieEn.pdf) |
| LK — Sri Lanka | LK | L:city~* → P:postcode~ | — | 9 / 25 | `Asia/Colombo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lkaEn.pdf) |
| LR — Liberia | LR | P:postcode~ → L:city~* | — | 15 / 224 | `Africa/Monrovia` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lbrEn.pdf) |
| LS — Lesotho | LS | L:city~* → P:postcode~ | — | 10 / 15 | `Africa/Maseru` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lsoEn.pdf) |
| LT — Lithuania | LT | P:postcode~* → L:city~* → A:county | — | 10 / 60 | `Europe/Vilnius` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ltuEn.pdf) |
| LU — Luxembourg | LU | P:postcode~* → L:city~* | — | 12 / 105 | `Europe/Luxembourg` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/luxEn.pdf) |
| LV — Latvia | LV | L:city~* → P:postcode~* | — | 43 / 587 | `Europe/Riga` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lvaEn.pdf) |
| LY — Libya | LY | **Fallback:** L:city~* | — | 22 / 1 | `Africa/Tripoli` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lbyEn.pdf); [postal review](fallback-address-review.md) |
| MA — Morocco | MA | P:postcode~ → L:city~* | — | 12 / 75 | `Africa/Casablanca` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/marEn.pdf) |
| MC — Monaco | MC | P:postcode~ → L:city~* | — | 1 / 0 | `Europe/Monaco` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mcoEn.pdf) |
| MD — Moldova | MD | P:postcode~ → L:city~* | — | 37 / 0 | `Europe/Chisinau` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mdaEn.pdf) |
| ME — Montenegro | ME | P:postcode~ → L:city~* | — | 25 / 0 | `Europe/Podgorica` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mneEn.pdf) |
| MF — St. Martin | MF | P:postcode~* → L:city~* | — | 0 / 0 | `America/Marigot` | [UPU selector grouping](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/glpEn.pdf) |
| MG — Madagascar | MG | P:postcode~ → L:city~* | — | 23 / 119 | `Indian/Antananarivo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mdgEn.pdf) |
| MH — Marshall Islands | MH | L:city~* → A:state* → P:ZIP* | — | 33 / 0 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mhlEn.pdf) |
| MK — North Macedonia | MK | P:postcode~ → L:city~* | — | 71 / 10 | `Europe/Skopje` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mkdEn.pdf) |
| ML — Mali | ML | **Fallback:** L:city~* | — | 11 / 50 | `Africa/Bamako` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mliEn.pdf); [postal review](fallback-address-review.md) |
| MM — Myanmar (Burma) | MM | L:city~* → P:postcode~ | — | 15 / 73 | `Asia/Yangon` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mmrEn.pdf) |
| MN — Mongolia | MN | L:city~* → A:province~ → P:postcode~ | — | 22 / 387 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mngEn.pdf) |
| MO — Macao SAR China | MO | No non-street component | — | 8 / 0 | `Asia/Macau` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/macEn.pdf) |
| MP — Northern Mariana Islands | MP | L:city~* → P:ZIP* | — | 4 / 12 | `Pacific/Saipan` | UPU match pending |
| MQ — Martinique | MQ | P:postcode~* → L:city~* | — | 1 / 1 | `America/Martinique` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mtqEn.pdf) |
| MR — Mauritania | MR | L:city~* | — | 15 / 55 | `Africa/Nouakchott` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mrtEn.pdf) |
| MS — Montserrat | MS | **Fallback:** L:city~* | — | 3 / 0 | `America/Montserrat` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/msrEn.pdf); [postal review](fallback-address-review.md) |
| MT — Malta | MT | L:city~* → P:postcode~ | — | 68 / 0 | `Europe/Malta` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mltEn.pdf) |
| MU — Mauritius | MU | P:postcode~ → L:city~* | — | 12 / 0 | `Indian/Mauritius` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/musEn.pdf) |
| MV — Maldives | MV | L:city~* → P:postcode~ | — | 21 / 0 | `Indian/Maldives` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mdvEn.pdf) |
| MW — Malawi | MW | L:city~* → S:sorting | — | 3 / 28 | `Africa/Blantyre` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mwiEn.pdf) |
| MX — Mexico | MX | D:neighborhood → P:postcode~* → L:city~* → A:state* | A=32 | 32 / 2471 | 12 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mexEn.pdf) |
| MY — Malaysia | MY | D:village_township → P:postcode~* → L:city~* → A:state* | A=16 | 16 / 144 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mysEn.pdf) |
| MZ — Mozambique | MZ | P:postcode~ → L:city~* → A:province~ | A=11 | 11 / 164 | `Africa/Maputo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mozEn.pdf) |
| NA — Namibia | NA | L:city~* → P:postcode~ | — | 14 / 47 | `Africa/Windhoek` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/namEn.pdf) |
| NC — New Caledonia | NC | P:postcode~* → L:city~* | — | 3 / 33 | `Pacific/Noumea` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/nclEn.pdf) |
| NE — Niger | NE | P:postcode~ → L:city~* | — | 8 / 67 | `Africa/Niamey` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/nerEn.pdf) |
| NF — Norfolk Island | NF | L:city~* → P:postcode~ | — | 0 / 0 | `Pacific/Norfolk` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/nfkEn.pdf) |
| NG — Nigeria | NG | D:suburb~ → L:city~* → P:postcode~ → A:state | A=37 | 37 / 785 | `Africa/Lagos` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ngaEn.pdf) |
| NI — Nicaragua | NI | P:postcode~ → L:city~* → A:department | A=17 | 17 / 153 | `America/Managua` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/nicEn.pdf) |
| NL — Netherlands | NL | P:postcode~* → L:city~* | — | 12 / 342 | `Europe/Amsterdam` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/nldEn.pdf) |
| NO — Norway | NO | P:postcode~* → L:post_town* | — | 15 / 357 | `Europe/Oslo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/norEn.pdf) |
| NP — Nepal | NP | L:city~* → P:postcode~ | — | 7 / 77 | `Asia/Kathmandu` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/nplEn.pdf) |
| NR — Nauru | NR | A:district* | A=14 | 14 / 0 | `Pacific/Nauru` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/nruEn.pdf) |
| NU — Niue | NU | **Fallback:** L:city~* | — | 0 / 0 | `Pacific/Niue` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/niuEn.pdf); [postal review](fallback-address-review.md) |
| NZ — New Zealand | NZ | D:suburb~ → L:town/city* → P:postcode~* | — | 17 / 66 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/nzlEn.pdf) |
| OM — Oman | OM | P:postcode~ → L:city~* | — | 11 / 61 | `Asia/Muscat` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/omnEn.pdf) |
| PA — Panama | PA | L:city~* → A:province~ | A=14 | 14 / 82 | `America/Panama` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/panEn.pdf) |
| PE — Peru | PE | L:district* → P:postcode~ → A:region* | A=26 | 26 / 196 | `America/Lima` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/perEn.pdf) |
| PF — French Polynesia | PF | P:postcode~* → L:city~* → A:island* | — | 5 / 48 | 3 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/pyfEn.pdf) |
| PG — Papua New Guinea | PG | L:city~* → P:postcode~ → A:province~* | A=22 | 22 / 87 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/pngEn.pdf) |
| PH — Philippines | PH | D:suburb~ → L:city~* → P:postcode~ → A:province~ | A=83 | 17 / 87 | `Asia/Manila` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/phlEn.pdf) |
| PK — Pakistan | PK | L:city~* → P:postcode~ | — | 7 / 157 | `Asia/Karachi` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/pakEn.pdf) |
| PL — Poland | PL | P:postcode~* → L:city~* | — | 16 / 380 | `Europe/Warsaw` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/polEn.pdf) |
| PM — St. Pierre & Miquelon | PM | P:postcode~* → L:city~* | — | 2 / 0 | `America/Miquelon` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/spmEn.pdf) |
| PN — Pitcairn Islands | PN | L:city~* → P:postcode~* | — | 0 / 0 | `Pacific/Pitcairn` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/pcnEn.pdf) |
| PR — Puerto Rico | PR | L:city~* → P:ZIP* | — | 78 / 902 | `America/Puerto_Rico` | UPU match pending |
| PS — Palestinian Territories | PS | **Fallback:** L:city~* | — | 2 / 16 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/pseEn.pdf); [postal review](fallback-address-review.md) |
| PT — Portugal | PT | P:postcode~* → L:city~* | — | 20 / 308 | 3 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/prtEn.pdf) |
| PW — Palau | PW | L:city~* → A:state* → P:ZIP* | — | 16 / 1 | `Pacific/Palau` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/plwEn.pdf) |
| PY — Paraguay | PY | P:postcode~ → L:city~* → A:province~ | A=18 | 18 / 246 | `America/Asuncion` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/pryEn.pdf) |
| QA — Qatar | QA | L:city~* | — | 8 / 0 | `Asia/Qatar` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/qatEn.pdf) |
| RE — Réunion | RE | P:postcode~* → L:city~* | — | 1 / 1 | `Indian/Reunion` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/reuEn.pdf) |
| RO — Romania | RO | P:postcode~* → L:city~* | — | 42 / 3181 | `Europe/Bucharest` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/rouEn.pdf) |
| RS — Serbia | RS | P:postcode~ → L:city~* | — | 2 / 25 | `Europe/Belgrade` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/srbEn.pdf) |
| RU — Russia | RU | L:city~* → A:region* → P:postcode~* | A=85 | 83 / 2648 | 26 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/rusEn.pdf) |
| RW — Rwanda | RW | L:city~* | — | 5 / 30 | `Africa/Kigali` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/rwaEn.pdf) |
| SA — Saudi Arabia | SA | L:city~* → P:postcode~ | — | 13 / 123 | `Asia/Riyadh` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sauEn.pdf) |
| SB — Solomon Islands | SB | **Fallback:** L:city~* | — | 10 / 183 | `Pacific/Guadalcanal` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/slbEn.pdf); [postal review](fallback-address-review.md) |
| SC — Seychelles | SC | L:city~* → A:island | A=27 | 28 / 0 | `Indian/Mahe` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sycEn.pdf) |
| SD — Sudan | SD | L:district* → P:postcode~ | — | 18 / 211 | `Africa/Khartoum` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sdnEn.pdf) |
| SE — Sweden | SE | P:postcode~* → L:post_town* | — | 21 / 290 | `Europe/Stockholm` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sweEn.pdf) |
| SG — Singapore | SG | L:city~* → P:postcode~* | — | 0 / 0 | `Asia/Singapore` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sgpEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| SH — St. Helena, Ascension & Tristan da Cunha | SH | L:city~* → P:postcode~* | — | 3 / 8 | `Atlantic/St_Helena` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/shnEn.pdf) |
| SI — Slovenia | SI | P:postcode~ → L:city~* | — | 212 / 17 | `Europe/Ljubljana` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/svnEn.pdf) |
| SJ — Svalbard & Jan Mayen | SJ | P:postcode~* → L:post_town* | — | 2 / 4 | `Arctic/Longyearbyen` | UPU match pending |
| SK — Slovakia | SK | P:postcode~* → L:city~* | — | 8 / 79 | `Europe/Bratislava` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/svkEn.pdf) |
| SL — Sierra Leone | SL | **Fallback:** L:city~* | — | 5 / 16 | `Africa/Freetown` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sleEn.pdf); [postal review](fallback-address-review.md) |
| SM — San Marino | SM | P:postcode~* → L:city~ | — | 9 / 0 | `Europe/San_Marino` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/smrEn.pdf) |
| SN — Senegal | SN | P:postcode~ → L:city~* | — | 14 / 45 | `Africa/Dakar` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/senEn.pdf) |
| SO — Somalia | SO | L:city~* → A:province~* → P:postcode~ | A=18 | 18 / 87 | `Africa/Mogadishu` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/somEn.pdf) |
| SR — Suriname | SR | L:city~* → A:province~ | A=10 | 10 / 68 | `America/Paramaribo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/surEn.pdf) |
| SS — South Sudan | SS | **Fallback:** L:city~* | — | 10 / 28 | `Africa/Juba` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ssdEn.pdf); [postal review](fallback-address-review.md) |
| ST — São Tomé & Príncipe | ST | **Fallback:** L:city~* | — | 2 / 7 | `Africa/Sao_Tome` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/stpEn.pdf); [postal review](fallback-address-review.md) |
| SV — El Salvador | SV | P:postcode~ → L:city~* → A:province~* | A=14 | 14 / 44 | `America/El_Salvador` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/slvEn.pdf) |
| SX — Sint Maarten | SX | **Fallback:** L:city~* | — | 0 / 0 | `America/Lower_Princes` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sxmEn.pdf); [postal review](fallback-address-review.md) |
| SY — Syria | SY | L:district* | — | 14 / 61 | `Asia/Damascus` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/syrEn.pdf) |
| SZ — Eswatini | SZ | L:city~* → P:postcode~ | — | 4 / 38 | `Africa/Mbabane` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/swzEn.pdf) |
| TA — Tristan da Cunha | SH + TA | L:city~* → P:postcode~ | — | — | — | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/taaEn.pdf); [special code](mapping-exceptions.md#special-territory-selectors--working-canonical-treatment) |
| TC — Turks & Caicos Islands | TC | L:city~* → P:postcode~* | — | 0 / 0 | `America/Grand_Turk` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tcaEn.pdf) |
| TD — Chad | TD | **Fallback:** L:city~* | — | 23 / 133 | `Africa/Ndjamena` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tcdEn.pdf); [postal review](fallback-address-review.md) |
| TF — French Southern and Antarctic Lands | TF | **Fallback:** L:city~* | — | 5 / 5 | `Indian/Kerguelen` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/atfEn.pdf); [postal review](fallback-address-review.md) |
| TG — Togo | TG | **Fallback:** L:city~* | — | 5 / 30 | `Africa/Lome` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tgoEn.pdf); [postal review](fallback-address-review.md) |
| TH — Thailand | TH | D:suburb~ → L:city~* → A:province~* → P:postcode~ | A=77 | 77 / 928 | `Asia/Bangkok` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/thaEn.pdf) |
| TJ — Tajikistan | TJ | P:postcode~ → L:city~* | — | 5 / 75 | `Asia/Dushanbe` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tjkEn.pdf) |
| TK — Tokelau | TK | **Fallback:** L:city~* | — | 3 / 0 | `Pacific/Fakaofo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tklEn.pdf); [postal review](fallback-address-review.md) |
| TL — Timor-Leste | TL | **Fallback:** L:city~* | — | 13 / 65 | `Asia/Dili` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tlsEn.pdf); [postal review](fallback-address-review.md) |
| TM — Turkmenistan | TM | P:postcode~ → L:city~* | — | 6 / 58 | `Asia/Ashgabat` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tkmEn.pdf) |
| TN — Tunisia | TN | P:postcode~ → L:city~* | — | 24 / 264 | `Africa/Tunis` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tunEn.pdf) |
| TO — Tonga | TO | **Fallback:** L:city~* | — | 5 / 23 | `Pacific/Tongatapu` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tonEn.pdf); [postal review](fallback-address-review.md) |
| TR — Türkiye | TR | P:postcode~* → L:district* → A:province~* | A=81 | 81 / 974 | `Europe/Istanbul` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/turEn.pdf) |
| TT — Trinidad & Tobago | TT | **Fallback:** L:city~* | — | 15 / 36 | `America/Port_of_Spain` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ttoEn.pdf); [postal review](fallback-address-review.md) |
| TV — Tuvalu | TV | L:city~* → A:island | A=9 | 8 / 1 | `Pacific/Funafuti` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tuvEn.pdf) |
| TW — Taiwan | TW | L:city~* → A:county* → P:postcode~* | A/L=22 | 4 / 22 | `Asia/Taipei` | UPU match pending |
| TZ — Tanzania | TZ | P:postcode~ → L:city~* | — | 31 / 170 | `Africa/Dar_es_Salaam` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tzaEn.pdf) |
| UA — Ukraine | UA | L:city~* → A:region → P:postcode~* | A=27 | 27 / 146 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ukrEn.pdf) |
| UG — Uganda | UG | **Fallback:** L:city~* | — | 4 / 122 | `Africa/Kampala` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ugaEn.pdf); [postal review](fallback-address-review.md) |
| UM — U.S. Outlying Islands | UM | L:city~* → A:state* → P:ZIP | A=9 | 9 / 0 | 2 refs | UPU match pending |
| US — United States | US | L:city~* → A:state* → P:ZIP* | A=62 | 51 / 3143 | 29 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/usaEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| UY — Uruguay | UY | P:postcode~ → L:city~* → A:province~ | A=19 | 19 / 124 | `America/Montevideo` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/uryEn.pdf) |
| UZ — Uzbekistan | UZ | P:postcode~ → L:city~* → A:province~ | — | 14 / 221 | 2 refs | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/uzbEn.pdf) |
| VA — Vatican City | VA | P:postcode~ → L:city~* | — | 0 / 0 | `Europe/Vatican` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/vatEn.pdf) |
| VC — St. Vincent & Grenadines | VC | L:city~* → P:postcode~ | — | 6 / 0 | `America/St_Vincent` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/vctEn.pdf) |
| VE — Venezuela | VE | L:city~* → P:postcode~ → A:state* | A=25 | 25 / 335 | `America/Caracas` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/venEn.pdf) |
| VG — British Virgin Islands | VG | L:city~ → P:postcode~ | — | 0 / 0 | `America/Tortola` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/vgbEn.pdf) |
| VI — U.S. Virgin Islands | VI | L:city~* → P:ZIP* | — | 3 / 20 | `America/St_Thomas` | UPU match pending |
| VN — Vietnam | VN | L:city~* → A:province~* → P:postcode~ | A=34 | 34 / 723 | `Asia/Ho_Chi_Minh` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/vnmEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| VU — Vanuatu | VU | **Fallback:** L:city~* | — | 6 / 0 | `Pacific/Efate` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/vutEn.pdf); [postal review](fallback-address-review.md) |
| WF — Wallis & Futuna | WF | P:postcode~* → L:city~* | — | 3 / 5 | `Pacific/Wallis` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/wlfEn.pdf) |
| WS — Samoa | WS | **Fallback:** L:city~* | — | 11 / 14 | `Pacific/Apia` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/wsmEn.pdf); [postal review](fallback-address-review.md) |
| XK — Kosovo | XK (explicit exception) | P:postcode~ → L:city~* | — | 7 / 38 | — | UPU match pending; [special code](mapping-exceptions.md#special-territory-selectors--working-canonical-treatment) |
| YE — Yemen | YE | **Fallback:** L:city~* | — | 22 / 333 | `Asia/Aden` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/yemEn.pdf); [postal review](fallback-address-review.md) |
| YT — Mayotte | YT | P:postcode~* → L:city~* | — | 17 / 0 | `Indian/Mayotte` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mytEn.pdf) |
| ZA — South Africa | ZA | D:suburb~ → L:city~* → P:postcode~* | — | 9 / 52 | `Africa/Johannesburg` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/zafEn.pdf); [country case](mapping-exceptions.md#country-cases-with-direct-evidence) |
| ZM — Zambia | ZM | P:postcode~ → L:city~* | — | 10 / 108 | `Africa/Lusaka` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/zmbEn.pdf) |
| ZW — Zimbabwe | ZW | L:city~* → A:province~ | A=10 | 10 / 62 | `Africa/Harare` | [UPU](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/zweEn.pdf) |

All rows still require the applicable national/address/provider/timezone/privacy acceptance in the country register. Matrix values were checked against their source definitions; no source count is a publication approval.
