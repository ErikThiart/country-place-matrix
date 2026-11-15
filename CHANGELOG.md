# Changelog

All notable changes to this project are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html). Data files carry
their own version in the file name and in a `version` field.

## [1.0.0] - 2026-11-15

### Added

- Country catalogue for 257 selectors and 250 canonical identities, built from
  Unicode CLDR 49 and the IANA Time Zone Database 2026e.
- Address format and postal subdivision data built from CommerceGuys Addressing,
  with postal capture overlays for 12 countries whose fallback format drops a
  postcode.
- Telephone numbering plan reference built from libphonenumber v9.0.42.
- Territory adapters for the CLDR territory selectors.
- Generated one-row-per-selector matrix and the findings documents.
- Builders with a check mode that fails when a derived file is stale.
- PHP library: checksum-verified catalogue loader and a town-name matcher for
  text extracted from web pages.
- Python and PHP test suites, static analysis, lint and CI.
