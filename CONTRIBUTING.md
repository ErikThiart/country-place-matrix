# Contributing

Corrections are welcome, especially from people who know a country's address
and administrative structure first hand.

## Reporting a data problem

Open an issue and include:

- the selector code, for example `IE`
- what the repository says and where (file and field)
- what is correct, with a link to an official or primary source and its date

A correction without a source cannot be merged. This project records what
sources say and where they conflict, so the source matters as much as the fix.

## Changing data

Derived files are generated. Do not edit them by hand.

1. Change the pinned source, the overlay, or the builder.
2. Rebuild with the matching script in `bin/`.
3. Run the checks below. The check mode of each builder must pass.
4. Include the regenerated files in the same pull request.

Updating a pinned source to a new release is a reviewed change. List what was
added, renamed, retired or split in the pull request description.

## Checks

```sh
python3 resources/data/country-sources/build.py --check
python3 bin/build-country-addresses.py --check
python3 bin/build-country-phones.py --check
python3 bin/build-country-readiness.py --check
python3 -m unittest discover -s tests -p "test_country_*.py"
ruff check && ruff format --check

composer install
composer check
```

`composer check` runs the code style check, PHPStan at level 8 and PHPUnit.

## Style

Python is formatted and linted with Ruff, configured in `pyproject.toml`.
PHP follows PER Coding Style 2.0 with strict types, configured in
`.php-cs-fixer.dist.php`. The PHP library is procedural by design: namespaced
functions with no classes and no runtime dependencies.

## Licence

By contributing you agree that code is released under the MIT licence and data
and documentation under CC BY 4.0, as described in `LICENSE` and
`LICENSE-DATA.md`.
