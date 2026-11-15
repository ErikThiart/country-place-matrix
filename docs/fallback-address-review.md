# Fallback-country postal review

Workbench · [Matrix](mapping-matrix.md) · [Source evidence](source-evidence.md) · [Mapping contract](mapping-contract.md)

Reviewed 25 October 2026 using full relevant extracted pages from **46 of the 51** candidates lacking dedicated library formats. These 46 references total 54 pages. Ambiguous Guyana/Tonga/Timor-Leste pages were also rendered and visually checked. Five cases lack an established standalone UPU sheet here: **AQ, CQ, DG, EA, IC**. Parent-format source routes for CQ/EA/IC are documented in [the special-code crosswalk](mapping-exceptions.md#explicit-parent-format-crosswalks); they do not need invented independent country formats.

These are dated source observations and proposed corrections, not certified current national rules or implemented forms. A sheet showing no postcode is not proof that a country has none. A PO-box sample does not locate business premises; postal recipient/phone details never become compulsory public directory fields. No raw PDF/contact details were copied into the repository.

## Priority field corrections

The upstream generic fallback contains locality/address lines but no postcode field. At least **12 fallback candidates below have explicit postcode schemes in their UPU references**. Their country overlays must preserve those fields instead of inheriting the fallback blindly. Final requiredness/normalisation needs current national confirmation; no unreviewed strict regex is approved.

| Candidate | Reference describes | Working correction |
| --- | --- | --- |
| CD | Seven digits | Add postcode plus province and dependent rural locality support |
| DJ | Five digits | Add postcode; distinguish locality and region |
| GH | Two-letter area prefix with numeric area component, plus a longer digital address | Preserve postcode/digital-address distinction; never truncate the longer identifier |
| GY | Seven-digit header; conflicting six-digit example | Add postcode capture; hold strict length rejection pending clarification |
| LC | LC-prefixed seven-character code with display spacing | Preserve raw value and review permitted spacing/normalisation |
| MS | MSR plus four digits | Add prefixed postcode capture |
| NU | Four-digit territory code | Add country-specific postcode handling; retain NU context |
| PS | Eight alphanumeric characters, examples with incomplete delivery suffix | Preserve partial/unknown information honestly; do not invent digits |
| TL | TL plus five digits, with a spaced example | Preserve raw/normalised distinction and missing-house-number cases |
| TT | Six digits | Add postcode capture with locality context |
| UG | Five digits | Add postcode capture for urban/rural and PO-box addresses |
| WS | WS plus four digits | Add prefixed postcode capture with island/locality context |

## Country-by-country observations

The date is the sheet’s printed revision month/year. Older sheets require current operator/national confirmation. Descriptions below paraphrase the reference and record our proposed handling.

| Code / candidate | Sheet date | Source observation and required handling | Reference |
| --- | --- | --- | --- |
| AO — Angola | 09/2004 | Street/locality example; no postcode shown. Old sheet cannot establish current absence of postcodes. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/agoEn.pdf) |
| AQ — Antarctica | — | Source still needed; use explicit country/territory review, not the generic postal form as an approved rule. | [UPU portal](https://www.upu.int/en/Postal-Solutions/Programmes-Services/Addressing-Solutions) |
| AW — Aruba | 01/2019 | Aruba-specific street/PO-box examples; preserve AW rather than using an obsolete Antilles identity. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/abwEn.pdf) |
| BI — Burundi | 11/2025 | Commune and province explicitly shown; use current national structure review, not generic City alone. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bdiEn.pdf) |
| BQ — Caribbean Netherlands | 05/2014 | Confirms separation of BES/CUW/SXM datasets; does not provide a complete island address form. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/besEn.pdf) |
| BV — Bouvet Island | 09/2004 | Identifies uninhabited context; no ordinary residential form is supplied. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bvtEn.pdf) |
| BW — Botswana | 09/2004 | PO box/private bag examples; postal box is not a public premises location. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/bwaEn.pdf) |
| BZ — Belize | 05/2021 | Premises, area and city have distinct address roles; no postcode shown in the example. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/blzEn.pdf) |
| CD — Congo - Kinshasa | 09/2022 | Explicit seven-digit postcode and province; rural examples need nested localities. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/codEn.pdf) |
| CF — Central African Republic | 03/2022 | PO box/locality examples; contact details in a postal sample do not become mandatory public listing fields. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cafEn.pdf) |
| CG — Congo - Brazzaville | 09/2004 | Street/locality example without postcode; do not turn lack of a code in an old sample into current national proof. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cogEn.pdf) |
| CK — Cook Islands | 11/2014 | Island is an explicit address component; retain CK context and useful island/locality identities. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cokEn.pdf) |
| CM — Cameroon | 07/2002 | PO-box/locality sample only; current street/region/postcode rules remain national evidence. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cmrEn.pdf) |
| CP — Clipperton Island | 08/2011 | Direct CP sheet gives five-digit postal routing and refers to France; does not prove ordinary premises eligibility. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cptEn.pdf) |
| CQ — Sark | — | No standalone UPU sheet established; reviewed GG/ES parent-format route and territory context documented. Provider/locality/timezone QA remains. | [UPU portal](https://www.upu.int/en/Postal-Solutions/Programmes-Services/Addressing-Solutions) |
| CW — Curaçao | 09/2026 | Direct Curaçao sheet contains Curaçao address examples; selector-associated Aruba PDF is the wrong content for this country. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/cuwEn.pdf) |
| DG — Diego Garcia | — | Source still needed; use explicit country/territory review, not the generic postal form as an approved rule. | [UPU portal](https://www.upu.int/en/Postal-Solutions/Programmes-Services/Addressing-Solutions) |
| DJ — Djibouti | 05/2020 | Explicit five-digit postcode with locality/region roles. Optional geocoded text in the sample does not require a new proprietary API. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/djiEn.pdf) |
| DM — Dominica | 07/2002 | Locality example without postcode; old sample is not proof no postcode system exists today. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/dmaEn.pdf) |
| EA — Ceuta & Melilla | — | No standalone UPU sheet established; reviewed GG/ES parent-format route and territory context documented. Provider/locality/timezone QA remains. | [UPU portal](https://www.upu.int/en/Postal-Solutions/Programmes-Services/Addressing-Solutions) |
| ER — Eritrea | 07/2002 | Street/locality sample; current national/address exceptions remain open. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/eriEn.pdf) |
| FJ — Fiji | 09/2004 | Dependent locality and town shown separately; do not collapse both into one required State. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/fjiEn.pdf) |
| GA — Gabon | 07/2002 | Examples split postal routing/delivery-office information around the locality; avoid a guessed flat numeric postcode regex. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gabEn.pdf) |
| GD — Grenada | 10/2026 | Village/municipality examples; geographic wording in a mailing instruction must not alter country identity. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/grdEn.pdf) |
| GH — Ghana | 03/2023 | Postal code and longer digital address are distinct; region/district/locality roles need explicit mapping. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ghaEn.pdf) |
| GM — Gambia | 07/2002 | Street/locality example without postcode; preserve text and obtain current national rules. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gmbEn.pdf) |
| GQ — Equatorial Guinea | 03/2023 | Province, sub-province and locality appear as separate components; preserve text until official type crosswalk is reviewed. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/gnqEn.pdf) |
| GY — Guyana | 08/2025 | Header specifies seven digits but one PO-box example has six; strict validation must wait for clarification. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/guyEn.pdf) |
| IC — Canary Islands | — | No standalone UPU sheet established; reviewed GG/ES parent-format route and territory context documented. Provider/locality/timezone QA remains. | [UPU portal](https://www.upu.int/en/Postal-Solutions/Programmes-Services/Addressing-Solutions) |
| LC — St. Lucia | 07/2019 | LC-prefixed alphanumeric postcode with significant display spacing; district/quarter roles need local labels. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lcaEn.pdf) |
| LY — Libya | 02/2012 | Street/locality example; dated sheet cannot certify current national metadata. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/lbyEn.pdf) |
| ML — Mali | 07/2002 | Different Bamako/other-locality examples; preserve dependent locality/address detail without inventing a province. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/mliEn.pdf) |
| MS — Montserrat | 06/2026 | Explicit MSR prefix plus four digits; library fallback would omit this postcode field. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/msrEn.pdf) |
| NU — Niue | 09/2017 | Explicit four-digit territory postcode reference; retain NU identity rather than assigning an NZ branch. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/niuEn.pdf) |
| PS — Palestinian Territories | 05/2025 | Eight-character alphanumeric scheme; examples use incomplete delivery suffix placeholders. Do not invent final delivery digits. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/pseEn.pdf) |
| SB — Solomon Islands | 03/2005 | Island/province-style names and locality sample; verify actual current types and islands separately. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/slbEn.pdf) |
| SL — Sierra Leone | 07/2002 | Street/locality sample only; current regional/address rules require further evidence. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sleEn.pdf) |
| SS — South Sudan | 01/2013 | Contact address only; insufficient to approve a country-specific address form. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ssdEn.pdf) |
| ST — São Tomé & Príncipe | 09/2004 | Locality example only; no comprehensive postal/admin rule supplied. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/stpEn.pdf) |
| SX — Sint Maarten | 11/2011 | Direct Sint Maarten sheet confirms distinct identity/operator; selector-associated Aruba PDF is not an SX address specification. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/sxmEn.pdf) |
| TD — Chad | 09/2004 | PO-box/locality example; country-specific street and administrative validation still open. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tcdEn.pdf) |
| TF — French Southern and Antarctic Lands | 08/2011 | Special uninhabited-territory context; no ordinary residential form supplied. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/atfEn.pdf) |
| TG — Togo | 03/2005 | PO-box/locality example only; preserve real operating location separately from mailing address. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tgoEn.pdf) |
| TK — Tokelau | 03/2005 | Refers address formatting to New Zealand but lists distinct islands; TK identity must remain separate. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tklEn.pdf) |
| TL — Timor-Leste | 08/2026 | TL prefix plus five digits; sheet shows a spaced variant and notes missing house numbers. Preserve raw text; do not require a fabricated number. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tlsEn.pdf) |
| TO — Tonga | 07/2002 | Sheet heading associates Clipperton with Tonga; quarantine that association as an anomaly, not a geographic parent. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/tonEn.pdf) |
| TT — Trinidad & Tobago | 05/2014 | Explicit six-digit postcode with locality and dependent locality examples. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ttoEn.pdf) |
| UG — Uganda | 01/2026 | Explicit five-digit postcode and urban/rural/locality examples; fallback would incorrectly omit the field. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/ugaEn.pdf) |
| VU — Vanuatu | 03/2005 | Contact address only; insufficient for full national address approval. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/vutEn.pdf) |
| WS — Samoa | 05/2014 | Explicit WS prefix plus four digits; locality/sub-locality/island roles remain distinct. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/wsmEn.pdf) |
| YE — Yemen | 03/2005 | Governorate list and contact address only; old sheet does not establish current administrative boundaries. | [country sheet](https://www.upu.int/UPU/media/upu/PostalEntitiesFiles/addressingUnit/yemEn.pdf) |

## Source anomalies and maintenance

The UPU selector associates CW/SX with the Aruba sheet and CP with French Polynesia. Content inspection did not establish those PDFs as the right country specifications. Separate **direct CW, SX and CP sheets were found, fetched as PDFs and checked**; the matrix now links those instead. BV, NU, PS and TK also have verified direct sheets even though absent from the inspected selector. Do not infer coverage from selector labels or construct an unverified PDF URL.

The Tonga heading mentioning Clipperton and the Guyana digit-count contradiction are retained as source anomalies. Neither can alter canonical geography or approve a strict validator. The correction record needs a current national/operator source before the affected rule is treated as settled. Other unreviewed sheets can contain similar errors; primary-source status is evidence, not infallibility.

All 51 rows remain unready for public activation until applicable address/admin/locality/provider/timezone/privacy checks pass. P markers in the country register mean postal-reference content reviewed, not passed country QA.
