<?php

declare(strict_types=1);

namespace ErikThiart\CountryPlaceMatrix;

/**
 * Find a town name in text extracted from a web page, and cut a verbatim quote around it.
 *
 * Page text taken from HTML joins block elements without a space ("High StreetFelixstoweIP11"), and many town
 * names are also ordinary words or parts of words (Bath, Ely, Rye, Sale). A plain substring search is wrong
 * in both directions. These functions apply explicit boundary rules instead.
 */

/**
 * Character offset of the first place $town is named as a word in $text, or null.
 *
 * Case-insensitive, but never inside a longer word ("bathroom" is not Bath, "likely" is not Ely, "Ryedale" is
 * not Rye). A capital right after a letter or digit, or a capital or digit right after the town, still counts
 * as a boundary, because that is what joined blocks look like ("CLGreenfordMiddlesex", "Hounslow020 3886 1313").
 * A lowercase word that is also a town ("a great deal") still matches.
 */
function town_at(string $text, string $town): ?int
{
    $town = trim($town);
    if ($town === '') {
        return null;
    }
    if (!preg_match_all('/' . preg_quote($town, '/') . '/iu', $text, $m, PREG_OFFSET_CAPTURE)) {
        return null;
    }
    foreach ($m[0] as [$hit, $byte]) {
        $before = $byte > 0 ? mb_substr(substr($text, max(0, $byte - 4), min(4, $byte)), -1) : '';
        $after = mb_substr(substr($text, $byte + strlen($hit), 4), 0, 1);
        $first = mb_substr($hit, 0, 1);
        $capital = mb_strtoupper($first) === $first && mb_strtolower($first) !== $first;
        // a letter or digit before is part of another word, unless the hit starts with a capital (a joined block)
        if ($before !== '' && !$capital && preg_match('/[\p{L}\p{N}]/u', $before)) {
            continue;
        }
        if ($after !== '' && preg_match('/\p{Ll}/u', $after)) {
            continue;
        }

        return mb_strlen(substr($text, 0, $byte));
    }

    return null;
}

function has_town(string $text, string $town): bool
{
    return town_at($text, $town) !== null;
}

/** The text from $pad characters before $pos to $pad after the needle, trimmed to whole words but never into the needle. */
function window_at(string $text, int $pos, int $len, int $pad): string
{
    $start = max(0, $pos - $pad);
    $lead = $pos - $start;
    $window = mb_substr($text, $start, $lead + $len + $pad);
    $cutStart = 0;
    if ($start > 0 && ($space = mb_strpos($window, ' ')) !== false && $space < $lead) {
        $cutStart = $space + 1;
    }
    $end = mb_strlen($window);
    if ($start + $end < mb_strlen($text) && ($space = mb_strrpos($window, ' ')) !== false && $space >= $lead + $len) {
        $end = $space;
    }

    return trim(mb_substr($window, $cutStart, $end - $cutStart));
}

/**
 * True when a piece of page text reads like a postal address: a UK-style postcode, or a numbered street.
 * With $townThenCode set, a town followed by a four-digit code also counts (the South African pattern).
 * A year or a phone number next to a town is not an address.
 */
function address_like(string $s, string $town = '', bool $townThenCode = false): bool
{
    if (preg_match('/\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b/', $s)) {
        return true;
    }
    $street = implode('|', [
        'Road', 'Rd', 'Street', 'St', 'Avenue', 'Ave', 'Lane', 'Ln', 'Drive', 'Dr', 'Way', 'Close', 'Crescent',
        'Place', 'Square', 'Terrace', 'Parade', 'Row', 'Hill', 'Gardens', 'Court', 'Boulevard', 'Highway',
        'Weg', 'Straat', 'Laan', 'Rylaan', 'Industrial Estate', 'Business Park', 'Retail Park',
    ]);
    if (preg_match('/\b\d{1,4}[A-Za-z]?,?\s+(?:[\p{Lu}][\p{L}\'.-]*\s+){1,4}(?:' . $street . ')\b/u', $s)) {
        return true;
    }

    return $town !== '' && $townThenCode && preg_match('/' . preg_quote($town, '/') . ',?\s*\d{4}\b/iu', $s) === 1;
}

/**
 * Location evidence for a town: a verbatim window around a place where the page names it.
 *
 * The first mention is often a list of areas served or a marketing heading. This walks up to 12 mentions and
 * prefers one that reads like an address. Windows with prices, reviews or sale text are skipped, because that
 * text changes and a quote that changes stops being evidence. Null when the page never names the town as a word.
 */
function town_coverage(string $text, string $town, int $pad = 45, bool $townThenCode = false): ?string
{
    $first = town_at($text, $town);
    if ($first === null) {
        return null;
    }
    $best = window_at($text, $first, mb_strlen($town), $pad);
    if (!quote_is_stable($best)) {
        $best = null;
    }
    $offset = $first;
    for ($tries = 0; $tries < 12 && ($best === null || !address_like($best, $town, $townThenCode)); $tries++) {
        $next = town_at(mb_substr($text, $offset + 1), $town);
        if ($next === null) {
            break;
        }
        $offset += 1 + $next;
        $window = window_at($text, $offset, mb_strlen($town), $pad);
        if (quote_is_stable($window) && address_like($window, $town, $townThenCode)) {
            return $window;
        }
        if ($best === null && quote_is_stable($window)) {
            $best = $window;
        }
    }

    return $best;
}

/**
 * False when a piece of page text is likely to change: prices, reviews, testimonials or sale wording.
 * A quote taken from text that changes stops being evidence when the page is next edited.
 */
function quote_is_stable(string $s): bool
{
    return preg_match('/[£$€]|\b(?:testimonials?|reviews?|asking price|for sale|per month)\b/iu', $s) !== 1;
}
