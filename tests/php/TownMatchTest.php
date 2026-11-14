<?php

declare(strict_types=1);

namespace ErikThiart\CountryPlaceMatrix\Tests;

use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

use function ErikThiart\CountryPlaceMatrix\address_like;
use function ErikThiart\CountryPlaceMatrix\has_town;
use function ErikThiart\CountryPlaceMatrix\town_at;
use function ErikThiart\CountryPlaceMatrix\town_coverage;
use function ErikThiart\CountryPlaceMatrix\window_at;

final class TownMatchTest extends TestCase
{
    /** @return iterable<string, array{string, string}> */
    public static function textsThatDoNotNameTheTown(): iterable
    {
        yield 'Bath inside bathroom' => ['Our bathroom fitters cover the county.', 'Bath'];
        yield 'Ely inside likely' => ['It is likely to rain.', 'Ely'];
        yield 'Sale inside Salesforce' => ['We use Salesforce for bookings.', 'Sale'];
        yield 'Rye inside Ryedale' => ['Visit Ryedale for the day.', 'Rye'];
        yield 'lowercase letters after the town' => ['Nailpro, Felixstowepolicy', 'Felixstowe'];
        yield 'empty town' => ['Any text at all.', ''];
        yield 'empty text' => ['', 'Bath'];
    }

    #[DataProvider('textsThatDoNotNameTheTown')]
    public function testTownInsideAnotherWordIsNotAMatch(string $text, string $town): void
    {
        self::assertFalse(has_town($text, $town));
        self::assertNull(town_at($text, $town));
    }

    /** @return iterable<string, array{string, string}> */
    public static function textsThatNameTheTown(): iterable
    {
        yield 'a word in a sentence' => ['Find us at 2 High Street, Bath BA1 1AA.', 'Bath'];
        yield 'possessive' => ["Felixstowe's best cafe.", 'Felixstowe'];
        yield 'lowercase town standing alone' => ['139 whitmore avenue grays RM162HU', 'Grays'];
        yield 'upper case text' => ['WE ARE IN WEMBLEY PARK', 'Wembley'];
        yield 'digit directly after the town' => ['Laser Clinic Hounslow020 3886 1313', 'Hounslow'];
        yield 'capital after letters is a joined block' => ['Dip Trans CLGreenfordMiddlesex', 'Greenford'];
        yield 'joined address block' => ['12 High StreetFelixstoweIP11 7AA', 'Felixstowe'];
        yield 'multibyte text before the town' => ['Café Zürich, Bath', 'Bath'];
    }

    #[DataProvider('textsThatNameTheTown')]
    public function testTownNamedAsAWordIsAMatch(string $text, string $town): void
    {
        self::assertTrue(has_town($text, $town));
    }

    public function testOffsetIsInCharactersNotBytes(): void
    {
        self::assertSame(13, town_at('Café Zürich, Bath', 'Bath'));
    }

    public function testWindowNeverCutsIntoTheTownName(): void
    {
        $text = str_repeat('x', 60) . 'Bury St Edmunds is a market town with a long history of trade and many shops around it.';
        $at = town_at($text, 'Bury St Edmunds');

        self::assertNotNull($at);
        self::assertStringContainsString('Bury St Edmunds is', window_at($text, $at, mb_strlen('Bury St Edmunds'), 45));
        self::assertSame('Leeds', window_at('We are based in Leeds today', 16, 5, 3));
    }

    public function testCoveragePrefersAnAddressOverAListOfAreas(): void
    {
        $page = 'We serve Ipswich, Felixstowe, Woodbridge and Colchester with fast repairs. '
            . str_repeat('Good work every day. ', 8)
            . 'Visit our shop at 14 Hamilton Road, Felixstowe IP11 7AX or call us.';

        self::assertStringContainsString('IP11 7AX', (string) town_coverage($page, 'Felixstowe'));
    }

    public function testCoverageSkipsUnstableText(): void
    {
        $page = 'Rated 5 stars in 40 reviews across Felixstowe this year. '
            . str_repeat('Good work every day. ', 8)
            . 'Our workshop is in Felixstowe near the docks.';

        self::assertStringNotContainsString('reviews', (string) town_coverage($page, 'Felixstowe'));
    }

    public function testCoverageIsNullWhenTheTownIsNotNamed(): void
    {
        self::assertNull(town_coverage('Our bathroom team', 'Bath'));
    }

    public function testAddressLikeText(): void
    {
        self::assertTrue(address_like('14 Hamilton Road, Felixstowe'));
        self::assertTrue(address_like('Felixstowe IP11 7AX'));
        self::assertFalse(address_like('Serving Felixstowe since 1998'));
        self::assertFalse(address_like('Call Felixstowe 01394 000000'));
        self::assertFalse(address_like('Main Road, Paarl, 7646', 'Paarl'));
        self::assertTrue(address_like('Main Road, Paarl, 7646', 'Paarl', true));
    }
}
