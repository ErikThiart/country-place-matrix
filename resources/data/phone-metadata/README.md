# Telephone numbering reference

This retained source is Google libphonenumber **v9.0.42**, pinned to commit
`8d8d75272c351b60b87163db5328e439c53a6b56`, published 27 October 2026.
`manifest.json` records official immutable URLs, byte counts, SHA-256 hashes and
the **Apache-2.0** license. Preserve the accompanying upstream license and XML
copyright notices when redistributing the source or derived JSON.

From the repository root:

```sh
python3 bin/build-country-phones.py
python3 bin/build-country-phones.py --check
python3 -m unittest discover -s tests -p test_country_phones.py
```

Rebuilding is offline by default. `--fetch-sources` retrieves only the exact
reviewed commit and requires every retained hash to match. To update, review an
official release, its region/prefix changes and license, deliberately update the
manifest and retained snapshot, rebuild, and inspect the generated diff/tests.
An upstream new region requires explicit reconciliation with the country catalog.

The source has **245 geographic regions and nine non-geographic calling plans**.
All 257 selectors are represented; direct plans include AC, TA and XK.
Twelve selectors have no direct upstream region: AQ, BV, CP, CQ, DG, EA, GS, HM,
IC, PN, TF and UM. Their calling-code hint remains null. A canonical geography
reference is retained separately and is **not** applied as a numbering fallback.
Non-geographic region `001` is never offered as a listing country. Shared calling
codes and main-region metadata remain explicit. Retired AN/CS require a country
choice, while the existing UK→GB alias policy remains sourced to the country
catalog; neither becomes a new phone region.

The derived JSON preserves national-number patterns, possible/local-only lengths,
prefix transformation rules, format templates and illustrative examples as text.
Leading zeros are significant. Examples are upstream documentation, **not contact
destinations**; do not call them. This is not number assignment, reachability,
ownership or national/provider acceptance. It does not change the application's
international phone input contract. Business contact numbers can legitimately
belong to a different numbering region from their address. Consumers needing a
parser should use a maintained libphonenumber implementation rather than turn
these reference regular expressions into a homegrown validator.
