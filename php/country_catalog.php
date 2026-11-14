<?php

declare(strict_types=1);

namespace ErikThiart\CountryPlaceMatrix;

use DateTimeZone;
use RuntimeException;
use UnexpectedValueException;

/**
 * The country catalogue: canonical identities, selectors, aliases and the timezone inventory.
 *
 * Identity metadata only. It supplies no national address rules and no approval to use a country.
 * The catalogue file and every pinned source file it was built from are verified by SHA-256 before
 * anything is returned, so a modified or partly updated data directory fails loudly.
 *
 * @return array<string, mixed>
 *
 * @throws RuntimeException when a file is missing or a checksum does not match
 * @throws UnexpectedValueException when the catalogue is structurally invalid
 */
function country_catalog(): array
{
    static $catalog;
    if ($catalog !== null) {
        return $catalog;
    }
    $file = dirname(__DIR__) . '/resources/data/country-catalog.v1.json';
    $data = country_catalog_read($file);
    $checksum = trim(country_catalog_read(dirname($file) . '/country-catalog.v1.sha256'));
    if (!preg_match('/^[a-f0-9]{64}$/D', $checksum) || !hash_equals($checksum, hash('sha256', $data))) {
        throw new RuntimeException('Country catalog checksum mismatch. Rebuild from reviewed pinned sources.');
    }
    $candidate = country_catalog_decode($data);
    foreach ($candidate['sources']['files'] as $source) {
        $sourceFile = dirname($file) . '/country-sources/' . $source['file'];
        $sourceHash = is_file($sourceFile) ? hash_file('sha256', $sourceFile) : false;
        if ($sourceHash === false || filesize($sourceFile) !== $source['bytes'] || !hash_equals($source['sha256'], $sourceHash)) {
            throw new RuntimeException('Pinned country source checksum mismatch: ' . $source['file']);
        }
    }

    return $catalog = $candidate;
}

/** @throws RuntimeException when the file cannot be read */
function country_catalog_read(string $file): string
{
    $data = is_file($file) ? file_get_contents($file) : false;
    if ($data === false) {
        throw new RuntimeException('Country catalog file is not readable: ' . basename($file));
    }

    return $data;
}

/**
 * Decode and validate catalogue JSON.
 *
 * @return array<string, mixed>
 *
 * @throws \JsonException when the text is not valid JSON
 * @throws UnexpectedValueException when the structure is invalid
 */
function country_catalog_decode(string $json): array
{
    $catalog = json_decode($json, true, 64, JSON_THROW_ON_ERROR);
    if (!is_array($catalog)) {
        throw new UnexpectedValueException('country_catalog_object_required');
    }
    country_catalog_validate($catalog);

    return $catalog;
}

/** @throws UnexpectedValueException with $code as its message when $valid is false */
function country_catalog_check(bool $valid, string $code): void
{
    if (!$valid) {
        throw new UnexpectedValueException($code);
    }
}

/**
 * Structural validation of a decoded catalogue. Throws on the first rule that fails.
 *
 * @param array<string, mixed> $catalog
 *
 * @throws UnexpectedValueException
 */
function country_catalog_validate(array $catalog): void
{
    country_catalog_check(
        is_string($catalog['version'] ?? null) && preg_match('/^[a-zA-Z0-9._-]{1,100}$/D', $catalog['version']) === 1,
        'invalid_catalog_version',
    );
    country_catalog_check(
        is_string($catalog['cldr_version'] ?? null)
        && preg_match('/^[a-zA-Z0-9._-]{1,100}$/D', $catalog['cldr_version']) === 1
        && is_string($catalog['tzdb_version'] ?? null)
        && preg_match('/^[a-zA-Z0-9._-]{1,100}$/D', $catalog['tzdb_version']) === 1,
        'invalid_catalog_revisions',
    );
    foreach (['countries', 'selectors', 'timezones', 'aliases'] as $key) {
        country_catalog_check(
            isset($catalog[$key]) && is_array($catalog[$key]) && !array_is_list($catalog[$key]),
            'invalid_catalog_' . $key,
        );
    }
    country_catalog_check(
        count($catalog['countries']) === 250 && count($catalog['selectors']) === 257,
        'unexpected_country_inventory',
    );
    $alpha3 = $numeric = [];
    $assigned = 0;
    foreach ($catalog['countries'] as $code => $country) {
        country_catalog_check(
            is_array($country) && preg_match('/^[A-Z]{2}$/D', (string) $code) === 1 && ($country['code'] ?? null) === $code,
            'invalid_country_identity',
        );
        country_catalog_check(
            is_string($country['name'] ?? null) && trim($country['name']) !== '' && mb_strlen($country['name']) <= 200,
            'invalid_country_name',
        );
        country_catalog_check(in_array($country['status'] ?? null, ['iso_assigned', 'exceptional'], true), 'invalid_country_status');
        if ($country['status'] === 'iso_assigned') {
            $assigned++;
            $a = $country['iso_alpha3'] ?? null;
            $n = $country['iso_numeric'] ?? null;
            country_catalog_check(
                is_string($a) && preg_match('/^[A-Z]{3}$/D', $a) === 1 && is_string($n) && preg_match('/^[0-9]{3}$/D', $n) === 1,
                'invalid_iso_crosswalk',
            );
            country_catalog_check(!isset($alpha3[$a]) && !isset($numeric[$n]), 'duplicate_iso_crosswalk');
            $alpha3[$a] = $numeric[$n] = true;
        } else {
            country_catalog_check(
                $code === 'XK'
                && array_key_exists('iso_alpha3', $country)
                && $country['iso_alpha3'] === null
                && array_key_exists('iso_numeric', $country)
                && $country['iso_numeric'] === null,
                'exceptional_country_has_iso_codes',
            );
        }
    }
    country_catalog_check(
        $assigned === 249 && ($catalog['countries']['XK']['status'] ?? null) === 'exceptional',
        'unexpected_iso_inventory',
    );
    $special = ['AC' => 'SH', 'CP' => 'FR', 'CQ' => 'GG', 'DG' => 'IO', 'EA' => 'ES', 'IC' => 'ES', 'TA' => 'SH'];
    foreach ($catalog['selectors'] as $code => $selector) {
        country_catalog_check(
            is_array($selector)
            && ($selector['code'] ?? null) === $code
            && is_string($selector['country_code'] ?? null)
            && isset($catalog['countries'][$selector['country_code']]),
            'invalid_selector_identity',
        );
        country_catalog_check(
            is_string($selector['label'] ?? null) && trim($selector['label']) !== '' && mb_strlen($selector['label']) <= 200,
            'invalid_selector_label',
        );
        country_catalog_check(is_bool($selector['requires_place_choice'] ?? null), 'invalid_place_choice');
        if (isset($special[$code])) {
            country_catalog_check(
                $selector['country_code'] === $special[$code]
                && ($selector['status'] ?? null) === 'cldr_selector'
                && ($selector['territory_code'] ?? null) === ($code === 'EA' ? null : $code)
                && $selector['requires_place_choice'] === ($code === 'EA'),
                'invalid_special_selector',
            );
        } else {
            country_catalog_check(
                isset($catalog['countries'][$code])
                && $selector['country_code'] === $code
                && ($selector['territory_code'] ?? null) === null
                && $selector['requires_place_choice'] === false
                && ($selector['status'] ?? null) === $catalog['countries'][$code]['status'],
                'invalid_canonical_selector',
            );
        }
    }
    country_catalog_check(
        !isset($catalog['selectors']['XA']) && !isset($catalog['selectors']['XB']) && !isset($catalog['selectors']['UK']),
        'pseudo_or_alias_selector',
    );
    foreach ($catalog['countries'] as $code => $country) {
        country_catalog_check(isset($catalog['selectors'][$code]), 'country_missing_selector');
    }
    foreach ($catalog['timezones'] as $name => $zone) {
        country_catalog_check(
            is_string($name)
            && is_array($zone)
            && ($zone['name'] ?? null) === $name
            && strlen($name) <= 64
            && preg_match('~^[A-Za-z0-9_+.-]+(?:/[A-Za-z0-9_+.-]+)*$~D', $name) === 1
            && in_array($zone['kind'] ?? null, ['zone', 'link'], true),
            'invalid_timezone_identity',
        );
        country_catalog_check(is_string($zone['canonical_name'] ?? null), 'invalid_timezone_link');
        $canonical = $catalog['timezones'][$zone['canonical_name']] ?? null;
        country_catalog_check(
            is_array($canonical)
            && ($canonical['kind'] ?? null) === 'zone'
            && is_string($canonical['name'] ?? null)
            && $canonical['name'] === ($canonical['canonical_name'] ?? null)
            && ($zone['kind'] !== 'zone' || $zone['canonical_name'] === $name),
            'invalid_timezone_link',
        );
    }
    country_catalog_check(
        isset($catalog['timezones']['UTC'])
        && is_array($catalog['timezone_inventory'] ?? null)
        && array_is_list($catalog['timezone_inventory'])
        && count($catalog['timezone_inventory']) <= 5000,
        'invalid_timezone_inventory',
    );
    $seen = [];
    foreach ($catalog['timezone_inventory'] as $row) {
        country_catalog_check(
            is_array($row)
            && is_string($row['country_code'] ?? null)
            && is_string($row['timezone'] ?? null)
            && ($catalog['countries'][$row['country_code']]['status'] ?? null) === 'iso_assigned'
            && isset($catalog['timezones'][$row['timezone']])
            && in_array($row['kind'] ?? null, ['zone.tab', 'zone1970.tab'], true),
            'invalid_country_timezone',
        );
        $key = $row['country_code'] . ':' . $row['timezone'] . ':' . $row['kind'];
        country_catalog_check(!isset($seen[$key]), 'duplicate_country_timezone');
        $seen[$key] = true;
    }
    foreach ($catalog['aliases'] as $code => $alias) {
        country_catalog_check(
            is_array($alias)
            && preg_match('/^[A-Z]{2}$/D', (string) $code) === 1
            && ($alias['code'] ?? null) === $code
            && !isset($catalog['selectors'][$code])
            && in_array($alias['action'] ?? null, ['normalise', 'retired', 'choose'], true),
            'invalid_country_alias',
        );
        country_catalog_check(
            $alias['action'] === 'normalise'
                ? $code === 'UK' && ($alias['country_code'] ?? null) === 'GB'
                : array_key_exists('country_code', $alias) && $alias['country_code'] === null,
            'unsafe_country_alias',
        );
        country_catalog_check(
            is_array($alias['replacement_selectors'] ?? null) && array_is_list($alias['replacement_selectors']),
            'invalid_alias_choices',
        );
        foreach ($alias['replacement_selectors'] as $replacement) {
            country_catalog_check(is_string($replacement) && isset($catalog['selectors'][$replacement]), 'unknown_alias_choice');
        }
    }
    foreach (['AN', 'CS', 'SU', 'YU'] as $code) {
        country_catalog_check(($catalog['aliases'][$code]['action'] ?? null) === 'choose', 'ambiguous_country_alias');
    }
    country_catalog_check(
        is_array($catalog['limits'] ?? null)
        && ($catalog['limits']['national_rules'] ?? null) === 'not_supplied'
        && ($catalog['limits']['phone_rules'] ?? null) === 'not_supplied'
        && ($catalog['limits']['timezone_inventory_is_context_approval'] ?? null) === false,
        'catalog_cannot_approve_national_policy',
    );
    country_catalog_check(
        is_array($catalog['sources'] ?? null)
        && ($catalog['sources']['catalog_version'] ?? null) === $catalog['version']
        && ($catalog['sources']['cldr_version'] ?? null) === $catalog['cldr_version']
        && ($catalog['sources']['tzdb_version'] ?? null) === $catalog['tzdb_version'],
        'catalog_source_revision_mismatch',
    );
    country_catalog_check(
        is_array($catalog['sources']['files'] ?? null)
        && array_is_list($catalog['sources']['files'])
        && count($catalog['sources']['files']) === 5,
        'invalid_catalog_sources',
    );
    $sourceFiles = [];
    foreach ($catalog['sources']['files'] as $source) {
        country_catalog_check(
            is_array($source)
            && is_string($source['file'] ?? null)
            && preg_match('/^[a-zA-Z0-9._-]+$/D', $source['file']) === 1
            && is_string($source['sha256'] ?? null)
            && preg_match('/^[a-f0-9]{64}$/D', $source['sha256']) === 1
            && is_int($source['bytes'] ?? null)
            && $source['bytes'] > 0
            && $source['bytes'] <= 2000000
            && is_string($source['url'] ?? null)
            && str_starts_with($source['url'], 'https://')
            && is_string($source['license'] ?? null)
            && trim($source['license']) !== ''
            && mb_strlen($source['license']) <= 1000,
            'invalid_catalog_source',
        );
        country_catalog_check(!isset($sourceFiles[$source['file']]), 'duplicate_catalog_source');
        $sourceFiles[$source['file']] = true;
    }
}

/**
 * The context for an exact selector code, or null.
 *
 * Aliases and retired codes are not selectors. Look those up in country_catalog()['aliases'] and
 * let the caller decide, because a retired code can have more than one successor.
 *
 * @return array{code: string, label: string, country_code: string, territory_code: string|null, requires_place_choice: bool, status: string}|null
 */
function country_catalog_context(string $selector): ?array
{
    return country_catalog()['selectors'][$selector] ?? null;
}

/**
 * The IANA timezones associated with a canonical country.
 *
 * This is unreviewed inventory, not a choice: a country with several zones still needs location
 * evidence to pick one. Territory selectors return an empty list and never inherit their parent's zones.
 *
 * @return list<array{iana_name: string, canonical_name: string, runtime_supported: bool, source_kinds: list<string>, inventory_revision: string, reviewed: bool}>
 */
function country_catalog_timezone_inventory(string $selector): array
{
    $catalog = country_catalog();
    $context = $catalog['selectors'][$selector] ?? null;
    if (!$context || $context['country_code'] !== $selector) {
        return [];
    }
    static $runtime;
    $runtime ??= array_fill_keys(DateTimeZone::listIdentifiers(DateTimeZone::ALL_WITH_BC), true);
    $items = [];
    foreach ($catalog['timezone_inventory'] as $row) {
        if ($row['country_code'] !== $selector) {
            continue;
        }
        $name = $row['timezone'];
        $items[$name] ??= [
            'iana_name' => $name,
            'canonical_name' => $catalog['timezones'][$name]['canonical_name'],
            'runtime_supported' => isset($runtime[$name]),
            'source_kinds' => [],
            'inventory_revision' => $catalog['tzdb_version'],
            'reviewed' => false,
        ];
        $items[$name]['source_kinds'][] = $row['kind'];
    }

    return array_values($items);
}
