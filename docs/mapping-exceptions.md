# National structures and mapping exceptions

Workbench · [All-country matrix](mapping-matrix.md) · [Mapping contract](mapping-contract.md)

Checked 25 October 2026. The rules below translate source differences into working product decisions. Counts describe the inspected reference or the cited dated authority, not a promise that all underlying places/addresses are imported or tested.

## Country cases with direct evidence

| Country | Administrative/browse meaning | Postal/form rule and mapping decision | Primary evidence |
| --- | --- | --- | --- |
| ZA — South Africa | Nine provinces; metro municipalities differ from district/local municipality structures | Province is a browse membership; source postal template uses suburb/locality/postcode and omits province. Add reviewed province data outside the library. Keep four-digit postcodes as text. | [Detailed ZA mapping](ZA.md), [government provinces](https://www.gov.za/about-sa/south-africas-provinces) |
| GB — United Kingdom | Four constituent nations with different local-government types; current authority and ceremonial/historic county are separate | Post town/postcode do not require a county. Library's flat 217 choices are not a current national authority tree; source postcode pattern includes special routing and cannot establish country. | [Detailed GB mapping](GB.md), [ONS](https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography) |
| US — United States | State/DC; counties and equivalents include parishes, boroughs and independent cities | Library's 62 mailing choices include AS/GU/MP/PR/VI, FM/MH/PW and AA/AE/AP. Territories/countries retain their own canonical contexts; military routing codes do not become public places. ZIP/postal city do not prove municipal membership. | [Census geographic definitions](https://www.census.gov/programs-surveys/popest/about/glossary/geo-terms.html), [inspected US root](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/resources/subdivision/US.json) |
| CA — Canada | Province/territory; census divisions/subdivisions describe specific statistical/municipal concepts | Library has 13 province/territory choices. Do not label all lower areas County; postal locality and bilingual names retain independent roles. Store postal code as text. | [Statistics Canada SGC hierarchy](https://www.statcan.gc.ca/en/subjects/standard/sgc/2021/introduction) |
| AU — Australia | State/territory, local government and suburb/locality are different; ABS statistical groupings are another view | Library has eight domestic postal choices; locality label is Suburb. Preserve special-territory routing, localities and multiple IANA zones; a single state timezone is insufficient. ABS Other Territories is not one real locality. | [ABS 2026 methodology](https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs/edition-4-july-2026-june-2031/methodology), [AU source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/resources/subdivision/AU.json) |
| IE — Ireland | Traditional address county, province and current local authority are separate | Library has 26 county choices; GeoNames levels contain four provinces and 31 second-level areas. Do not equate them. Support townland text; Eircode is a distinct field, with no synthetic value where absent. | [Government local authorities](https://www.gov.ie/en/department-of-housing-local-government-and-heritage/publications/your-council/), [IE source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/resources/subdivision/IE.json) |
| DE — Germany | Bundesland, district/independent city and municipality need national types | Germany has 16 Länder although the source postal form has no administrative-area field or subdivision root. Do not add a mandatory postal State field just to support regional browse. Keep leading-zero postcodes. | [Destatis Länder](https://www.destatis.de/DE/Themen/Laender-Regionen/Regionales/Gemeindeverzeichnis/Glossar/bundeslaender.html) |
| FR — France | INSEE regions, departments and communes, with special/overseas structures | Source postal template uses postcode/locality and optional sorting information; commune ID is not a postcode. National datasets covering overseas areas do not justify collapsing their directory country/territory identities into metropolitan FR. | [INSEE COG 2026](https://www.insee.fr/fr/information/8740222), [commune/postcode distinction](https://www.insee.fr/fr/information/1302169?question=quel-est-le-code-insee-de-ma-commune) |
| HK — Hong Kong | Three address areas contain 18 districts; root levels differ between providers | Library models Area → District, while GeoNames puts districts at ADM1. Preserve both types and local-script order; source form contains no postcode. Never manufacture 000000 or a province. | [Home Affairs district map](https://www.had.gov.hk/en/18_districts/my_map.htm), [HK source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/resources/subdivision/HK.json) |
| JP — Japan | Prefecture and local municipality/ward concepts; 47 source prefecture choices | Keep native-script format separate from international order. Source postcodes are seven digits with display hyphen; address lines must support blocks/buildings without demanding a Western street name/number split. | [Statistics Bureau prefecture context](https://www.stat.go.jp/english/data/nenkan/1431-03e.html), [JP source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/resources/subdivision/JP.json), [UPU addressing reference](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/jpnEn.pdf) |
| IN — India | States and union territories are distinct types; library currently has 36 combined choices | Source State label needs a State / Union territory product label after type review. Preserve six-digit PIN and native names; separate district/locality. A matching source count does not verify every boundary. | [IN source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/resources/subdivision/IN.json), [UPU country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/indEn.pdf) |
| AE — United Arab Emirates | Emirate is the administrative address role; library has seven choices | Template omits postcode and permits an optional locality. Support actual street/building/PO-box text where applicable; a postal box is not premises. Do not insert a fake ZIP or force City. | [AE source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/resources/subdivision/AE.json), [UPU country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/areEn.pdf) |
| SG — Singapore | Do not invent a province/county from a postal form or an absent GeoNames ADM1 list | Source defaults locality to Singapore, contains six-digit postcode and no region. Do not force an owner to choose a redundant city; any planning-area browse dataset needs its own reviewed type/source. | [Address definitions](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/src/AddressFormat/AddressFormatRepository.php), [UPU country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sgpEn.pdf) |
| VN — Vietnam | Provincial-level provinces and centrally run cities; review the 2025 two-tier changes | Government records 34 provincial-level units after reorganisation. Library and GeoNames ADM1 both have 34 entries, but that does not validate lower levels. Do not require an obsolete district or treat the legacy five/six-digit source regex as current postal authority. | [Government resolution, effective 12 June with new administrations operating 1 July 2025](https://cms.baochinhphu.vn/nghi-quyet-cua-quoc-hoi-ve-sap-xep-don-vi-hanh-chinh-cap-tinh-102250612191145158.htm), [VN source](https://raw.githubusercontent.com/commerceguys/addressing/e3ce66714cfa181b848533d926e8583261253c9e/resources/subdivision/VN.json) |

For all other candidates the matrix supplies actual source roles/counts and explicit gaps; their national administrative meanings remain a required review. No generic default is promoted to a verified local label.

## Special territory selectors — working canonical treatment

The source inventory mixes ordinary countries/territories with additional CLDR region codes. Preserve all candidates for review. Model these selectors as explicit territory context where appropriate; do not create duplicate listings or pretend every selector is an ordinary ISO country. Parent jurisdiction, postal routing, geocoder filter and timezone are separate reviewed fields.

| Selector | Working directory mapping | Address/provider consequence |
| --- | --- | --- |
| AC — Ascension Island | SH + territory AC | Dedicated library postal format AC; no GeoNames country/IANA own-country row. Confirm island lookup/timezone explicitly. |
| TA — Tristan da Cunha | SH + territory TA | Dedicated TA postal format; keep distinct island context and verify provider/zone. |
| CQ — Sark | GG + territory CQ | Present in CLDR 49 but absent from library/GeoNames country entries. Use a reviewed GG postal-format overlay plus Sark context; Guernsey Post supplies current Sark postal examples. No silent GB replacement. |
| IC — Canary Islands | ES + territory IC | Region/island/province relationships stay Spanish geography; generic source address fallback is not an approved local form. Restrict lookup to the islands. |
| EA — Ceuta & Melilla | ES + selected Ceuta or Melilla place | A combined source label is not one city or one contiguous boundary. Ask for the actual place before precise mapping. |
| CP — Clipperton Island | FR + territory CP, subject to current national review | UPU selector groups it with French Polynesia, but a verified direct CP sheet points to France and shows five-digit routing. Keep the distinction and confirm current national/premises eligibility; no ordinary residential assumptions. |
| DG — Diego Garcia | IO + territory DG as a source-mapping candidate; current jurisdiction requires confirmation | Provider/source grouping is not current legal-status evidence. Keep unresolved until the operating-date authority and lookup policy are checked. |
| XK — Kosovo | Explicit XK context with documented non-ISO code status | Do not convert to RS because a provider or timezone source lacks XK. Provider support and shared-zone mapping need their own evidence. |

These are reviewable product mappings, not completed jurisdiction/provider approval. See [CLDR region validity](https://raw.githubusercontent.com/unicode-org/cldr/96e54b273d2da4ec6fbad350ba19ff23fa24a588/common/validity/region.xml), [CLDR code semantics](https://unicode.org/reports/tr35/tr35.html), [UK Crown Dependencies reference](https://www.gov.uk/csv-preview/625009018fa8f54a905515bc/fcdo-crown-dependencies.csv) and [UPU country-sheet selector](https://www.upu.int/en/Postal-Solutions/Programmes-Services/Addressing-Solutions). None certifies a geocoding filter or resolves every current territorial dispute.

GG, JE and IM remain separate from GB; PR, GU, AS, MP and VI retain their own country/territory entries. Preserve BQ/CW/SX separately from NL, and reviewed French overseas entries separately from FR. Shared postal carriers, political associations, language, dialling codes or currency do not collapse directory identities. AQ/BV/HM/TF/UM and other special contexts need evidenced treatment for real business premises/service coverage; a dropdown entry does not imply normal postal delivery or public registration.

## Explicit parent-format crosswalks

For CQ, [Guernsey Post’s current branch directory](https://www.guernseypost.com/locations-opening-hours) identifies its Sark office with a GY10 postcode. The pinned GG template supports that postal structure. Working mapping is country GG + territory CQ + reviewed GG format, retaining Sark locality; a new CQ library country definition is not necessary merely to reuse GG formatting. The post-office postcode is an example, never a default assigned to every Sark business.

For IC/EA, [Spain’s INE province code table](https://ine.es/daco/daco42/codmun/cod_provincia.htm) and the pinned ES postal subdivision file establish the following explicit crosswalk. INE numeric codes and library keys belong to different namespaces; none is a global country code. These source pairs do not prove a postcode/pin belongs to a province.

| Chosen context | Postal seed key in ES file | INE province/city reference | Working country/format |
| --- | --- | --- | --- |
| Canary Islands → Las Palmas | GC | 35 — Palmas, Las | ES + territory IC; reviewed ES format |
| Canary Islands → Santa Cruz de Tenerife | TF | 38 — Santa Cruz de Tenerife | ES + territory IC; reviewed ES format |
| Ceuta | CE | 51 — Ceuta | ES + selected Ceuta place; reviewed ES format |
| Melilla | ML | 52 — Melilla | ES + selected Melilla place; reviewed ES format |

`TF` here is a Spanish postal seed key, not the country code for French Southern and Antarctic Lands. IC cannot become a single province, and EA cannot become a single city. Parent-format reuse still needs territory-specific field/requiredness review, bounded provider filters, localities and timezone/pin acceptance. Neither a shared format nor a successful code lookup passes those gates.

## Alias and regression cases

| Input/case | Required result |
| --- | --- |
| UK; United Kingdom; GB | One GB country identity; four constituent nations remain typed areas |
| South Africa; ZA; SA | ZA for the first two; SA is Saudi Arabia, not a South Africa code alias |
| Namibia; NA; blank/null | NA remains a real string code; it cannot be parsed as missing data |
| US state CA versus country CA | California and Canada keep different namespaces/context |
| Congo CG/CD; Korea KP/KR; Niger NE/Nigeria NG | Separate identities; ambiguous names need selection |
| AN or CS in old GeoNames data | Obsolete codes cannot create current countries or automatically select one successor |
| Swaziland/Eswatini; Turkey/Türkiye | Reviewed name aliases retain SZ/TR identity; no duplicate country |
| AC/TA within SH; Sark within GG | Preserve chosen territory and postal context; avoid duplicate branch identities |
| New or repeated town name | Resolve with country/type/current parent; no first-match assignment |
| Rural address/no postcode/no street number | Apply reviewed local rules and pin precision; no synthetic address fields |
| Overseas ZIP/postcode accepted by a mainland regex | Pattern match cannot override selected country/territory or prove physical location |
| Hidden home/service-area address | Public area/coverage only; no exact address, pin, direction link or inferred precise distance |

Each country still needs representative locality/address fixtures with expected canonical fields and actual provider results. This table defines acceptance cases; it does not claim those application tests ran.
