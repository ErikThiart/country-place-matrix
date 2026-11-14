<?php

declare(strict_types=1);

namespace ErikThiart\CountryPlaceMatrix\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;
use UnexpectedValueException;

use function ErikThiart\CountryPlaceMatrix\country_catalog;
use function ErikThiart\CountryPlaceMatrix\country_catalog_context;
use function ErikThiart\CountryPlaceMatrix\country_catalog_decode;
use function ErikThiart\CountryPlaceMatrix\country_catalog_timezone_inventory;

final class CountryCatalogTest extends TestCase
{
    public function testCatalogueLoadsWithVerifiedChecksums(): void
    {
        $catalog = country_catalog();

        self::assertCount(257, $catalog['selectors']);
        self::assertCount(250, $catalog['countries']);
        self::assertSame('2026e', $catalog['tzdb_version']);
    }

    public function testOrdinaryCountryIsItsOwnIdentity(): void
    {
        $context = country_catalog_context('GB');

        self::assertNotNull($context);
        self::assertSame('GB', $context['country_code']);
        self::assertNull($context['territory_code']);
    }

    /** @return iterable<string, array{string, string, string|null}> */
    public static function territorySelectors(): iterable
    {
        yield 'Ascension Island' => ['AC', 'SH', 'AC'];
        yield 'Tristan da Cunha' => ['TA', 'SH', 'TA'];
        yield 'Clipperton Island' => ['CP', 'FR', 'CP'];
        yield 'Sark' => ['CQ', 'GG', 'CQ'];
        yield 'Diego Garcia' => ['DG', 'IO', 'DG'];
        yield 'Canary Islands' => ['IC', 'ES', 'IC'];
        yield 'Ceuta and Melilla' => ['EA', 'ES', null];
    }

    #[DataProvider('territorySelectors')]
    public function testTerritorySelectorResolvesToCountryAndTerritory(string $selector, string $country, ?string $territory): void
    {
        $context = country_catalog_context($selector);

        self::assertNotNull($context);
        self::assertSame($country, $context['country_code']);
        self::assertSame($territory, $context['territory_code']);
    }

    public function testCeutaAndMelillaNeedAPlaceChoice(): void
    {
        self::assertTrue(country_catalog_context('EA')['requires_place_choice'] ?? false);
        self::assertFalse(country_catalog_context('IC')['requires_place_choice'] ?? true);
    }

    public function testAliasesAndRetiredCodesAreNotSelectors(): void
    {
        self::assertNull(country_catalog_context('UK'));
        self::assertNull(country_catalog_context('AN'));
        self::assertNull(country_catalog_context('gb'));
        self::assertSame('GB', country_catalog()['aliases']['UK']['country_code']);
        self::assertNull(country_catalog()['aliases']['AN']['country_code']);
    }

    public function testCodesThatLookLikeOtherThingsStayDistinct(): void
    {
        self::assertSame('Saudi Arabia', country_catalog_context('SA')['label'] ?? null);
        self::assertSame('Namibia', country_catalog_context('NA')['label'] ?? null);
        self::assertSame('South Africa', country_catalog_context('ZA')['label'] ?? null);
    }

    public function testTerritorySelectorInheritsNoTimezone(): void
    {
        self::assertSame([], country_catalog_timezone_inventory('IC'));
        self::assertSame([], country_catalog_timezone_inventory('UK'));
    }

    public function testCountryWithSeveralTimezonesListsThemUnreviewed(): void
    {
        $zones = country_catalog_timezone_inventory('AU');

        self::assertGreaterThan(1, count($zones));
        foreach ($zones as $zone) {
            self::assertFalse($zone['reviewed']);
            self::assertSame('2026e', $zone['inventory_revision']);
        }
    }

    public function testMalformedCatalogueIsRejected(): void
    {
        $this->expectException(UnexpectedValueException::class);
        country_catalog_decode('{"version":"x"}');
    }
}
