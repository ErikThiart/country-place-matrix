# country-place-matrix

[![CI](https://github.com/ErikThiart/country-place-matrix/actions/workflows/ci.yml/badge.svg)](https://github.com/ErikThiart/country-place-matrix/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC%20BY%204.0-blue.svg)](LICENSE-DATA.md)
[![PHP 8.2+](https://img.shields.io/badge/php-8.2%2B-777bb4.svg)](composer.json)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776ab.svg)](pyproject.toml)

A cross-checked reference of country, territory, address, telephone and timezone metadata for 257 country and territory selectors, with the scripts that build it from pinned public sources and a small PHP library for using it.

It exists because the public sources disagree with each other, and no single one is safe to build a worldwide address or location form on. This repository records what each source says for every selector, where they conflict, and exactly what is still unknown.

## What is in the matrix

| | Count |
| --- | ---: |
| Country and territory selectors | 257 |
| Canonical identities (249 ISO codes plus XK) | 250 |
| Dedicated address formats | 206 |
| Address formats inherited from a parent | 5 |
| Generic address formats, each needing review | 46 |
| Postal subdivision references | 12,075 |
| Administrative and populated-place records counted | 5,778,961 |
| Selectors with a direct telephone region | 245 |
| Selectors with no direct timezone entry | 10 |

The full table, one row per selector, is [docs/country-data-matrix.md](docs/country-data-matrix.md). It is generated. Do not edit it by hand.

## Findings

The reasoning and the per-country cases are in [docs/](docs/):

- [mapping-contract.md](docs/mapping-contract.md): how the sources join, and the rules for doing it safely.
- [mapping-matrix.md](docs/mapping-matrix.md): the source-to-source mapping for all 257 candidates.
- [mapping-exceptions.md](docs/mapping-exceptions.md): countries and territories where the sources conflict or need special treatment.
- [fallback-address-review.md](docs/fallback-address-review.md): what reading the postal references found for countries with no dedicated address format.
- [source-evidence.md](docs/source-evidence.md): versions, hashes and what was actually checked.
- [GB.md](docs/GB.md) and [ZA.md](docs/ZA.md): two worked country reviews.

A few examples of what the cross-check found:

- The address library advertises subdivision data for 62 countries. The files contain 63.
- Its United Kingdom list still has Cumbria and lacks the two authorities that replaced it.
- Hong Kong has three address areas in one source and 18 districts in another. Ireland has 26 address counties in one and four provinces with 31 second-level areas in the other. They cannot be joined by level number.
- Ten selectors have no direct timezone entry. They are not given UTC and do not inherit a parent's zone.
- "UK" is an alias for GB. "SA" is Saudi Arabia, not South Africa.

## Layout

```
resources/data/
  country-catalog.v1.json            identities, selectors, aliases, timezone inventory
  country-address-metadata.v1.json   address format summary per selector
  country-addresses.v1.json          full address formats and subdivisions
  country-phone-reference.v1.json    telephone numbering plan reference
  territory-adapters.v1.json         roots for territory selectors
  country-sources/                   pinned CLDR and tzdb inputs, and the catalogue builder
  addressing/                        pinned address sources and postal evidence
  phone-metadata/                    pinned libphonenumber metadata
  geonames/                          manifest and source pins (place shards not included)
bin/                                 build scripts
php/                                 catalogue loader and town-name matcher
docs/                                the matrix and the findings
tests/                               Python tests, and PHPUnit tests in tests/php
```

## Verify

The data checks run offline against the pinned inputs. They need Python 3.10 or later and PHP 8.2 or later with mbstring.

```sh
python3 resources/data/country-sources/build.py --check
python3 bin/build-country-addresses.py --check
python3 bin/build-country-phones.py --check
python3 bin/build-country-readiness.py --check
python3 -m unittest discover -s tests -p "test_country_*.py"
```

Each `--check` fails if a derived file no longer matches its pinned sources. Running a builder without `--check` rebuilds its output.

The PHP library has its own checks: code style, PHPStan at level 8 and PHPUnit.

```sh
composer install
composer check
```

The same checks run in CI on every push, across Python 3.10 and 3.13 and PHP 8.2 to 8.4.

The GeoNames place shards are about 250 MB and are not in this repository. The manifest is, and that is all the matrix needs. To rebuild the shards from the pinned downloads:

```sh
python3 bin/build-geonames-reference.py --fetch
```

`bin/build-territory-adapters.py` needs those shards.

## PHP

Two files of namespaced functions. No classes and no runtime dependencies.

The package is not on Packagist. Install it from the repository:

```json
{
    "repositories": [
        { "type": "vcs", "url": "https://github.com/ErikThiart/country-place-matrix" }
    ],
    "require": {
        "erikthiart/country-place-matrix": "^1.0"
    }
}
```

```php
use function ErikThiart\CountryPlaceMatrix\country_catalog;
use function ErikThiart\CountryPlaceMatrix\country_catalog_context;
use function ErikThiart\CountryPlaceMatrix\country_catalog_timezone_inventory;
use function ErikThiart\CountryPlaceMatrix\has_town;
use function ErikThiart\CountryPlaceMatrix\town_coverage;

country_catalog_context('IC');
// ['code' => 'IC', 'label' => 'Canary Islands', 'country_code' => 'ES', 'territory_code' => 'IC', ...]

country_catalog_context('UK');            // null: UK is an alias, not a selector
country_catalog()['aliases']['UK'];       // ['action' => 'normalise', 'country_code' => 'GB', ...]

country_catalog_timezone_inventory('IC'); // []: a territory selector inherits nothing

has_town('Our bathroom fitters cover the county.', 'Bath');   // false
has_town('12 High StreetFelixstoweIP11 7AA', 'Felixstowe');   // true

town_coverage($pageText, 'Felixstowe');
// a verbatim quote around the mention that reads most like an address
```

Without Composer, `require` the two files in `php/` directly.

`country_catalog()` verifies the catalogue checksum and the pinned source hashes before returning anything, and throws if a file is missing or changed.

`town_at()` finds a town name in text extracted from a web page. Such text joins block elements without spaces, and many town names are ordinary words or parts of words, so a substring search is wrong in both directions. The matcher applies explicit boundary rules. The cases are in [tests/php/TownMatchTest.php](tests/php/TownMatchTest.php).

## What this is not

- It is not a claim of national accuracy. A full row means reference data exists, not that it has been reviewed for that country.
- It does not validate an address or locate a business.
- It does not decide which country a disputed or changing territory belongs to. Territory selectors follow CLDR, and the mapping is a documented product choice.
- Unknown values stay unknown. A missing timezone, telephone region or postcode rule is recorded as missing and never filled with a default.

## Licence

Code is MIT, see [LICENSE](LICENSE). Derived data and documentation are CC BY 4.0, see [LICENSE-DATA.md](LICENSE-DATA.md). Third-party sources keep their own licences and attribution, see [NOTICE.md](NOTICE.md).

## Cite

See [CITATION.cff](CITATION.cff). The matrix came out of the work described in:

Thiart, E. (2026). Harness Engineering for AI-Written Business Listings. Zenodo. https://doi.org/10.5281/zenodo.24217719
