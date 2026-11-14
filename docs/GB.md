# GB — United Kingdom geography review draft

Country register · Geography specification

State: **research draft; full data/lookup/UX acceptance not completed**. Canonical country code GB; “UK” is a user/search alias, not a second duplicate country record. Review dependencies/territories through their own source/support entries instead of assuming they are all GB.

## Administrative distinctions

Support England, Scotland, Wales and Northern Ireland and the actual structures applicable within each. [ONS administrative geography](https://www.ons.gov.uk/methodology/geography/ukgeographies/administrativegeography) provides the primary overview. England includes counties and unitary/borough arrangements; Scotland uses council areas; Wales and Northern Ireland have their own authorities/districts. A place can have a ceremonial/historic county association that is not its current administrative parent.

Use the appropriate types/labels and authoritative identifiers, with one useful canonical browse path. Do not make every listing choose a “County” or fabricate one for places governed differently. A business's service areas can cover multiple reviewed places without claiming premises in all of them.

## Postal and public address draft

Street/building and optional locality → post town → postcode → country as appropriate. County is optional: the [Post Office](https://www.postoffice.co.uk/mail/how-to-address-mail) says it is unnecessary with town and postcode. Postal town, postcode area and administrative locality are different. Preserve the user's supplied address while normalising display using reviewed country metadata.

Store postcode as text, normalise casing/spacing appropriately and do not treat a matching pattern as proof the address exists. Validate real special cases against the selected source/provider rather than inventing a comprehensive regex. Business hours use the branch's IANA zone and current DST rules.

## Source crosswalk checked 25 October 2026

| Constituent nation | GeoNames ADM1 key | GeoNames ID | Area labels below it |
| --- | --- | --- | --- |
| England | GB.ENG | 6269131 | Applicable county/district, unitary authority or metropolitan/London borough; type depends on the actual location |
| Scotland | GB.SCT | 2638360 | Council area |
| Wales | GB.WLS | 2634895 | Principal/local authority, with actual county/county-borough type retained |
| Northern Ireland | GB.NIR | 2641364 | Local government district |

Reference: [GeoNames ADM1 source](https://download.geonames.org/export/dump/admin1CodesASCII.txt), with snapshot/hash in [source evidence](source-evidence.md). These source keys are not interchangeable with ISO or ONS codes. England/Scotland/Wales/Northern Ireland are typed areas inside the GB directory context, rather than four duplicate country records.

The inspected library subdivision root contains **217** postal choices, including `CMA` = Cumbria, with no Cumberland or Westmorland and Furness entries. This can retain postal/historic meaning but cannot define current local government. ONS identifies [Cumberland, E06000063](https://www.ons.gov.uk/explore-local-statistics/areas/E06000063-cumberland) and [Westmorland and Furness, E06000064](https://www.ons.gov.uk/explore-local-statistics/areas/E06000064-westmorland-and-furness), replacing their predecessor districts in 2023. A historic Cumbria query may remain useful; it must not assign a business to a current Cumbria county council.

Working editor: GB → constituent nation/locality context → address lines/post town/postcode; derive or ask to confirm the actual browse authority only when needed. Optional postal county text remains separate. A postcode pattern accepting GY/JE/IM or other special routing cannot turn GG/JE/IM premises into GB locations. Confirm Europe/London against branch location and runtime tzdb; do not apply it automatically to dependencies or overseas territories.

## Required evidence before ready

Review all four nations, London borough/unitary/two-tier examples, rural/dependent localities, postcode formatting and exceptional addresses. Confirm source/data licences and boundary mapping; test provider suggestions and inaccurate/unknown addresses, private home/service-area locations, aliases and canonical URLs. Record reviewer/date/version and known gaps. Country activation is not approved by this research draft.
