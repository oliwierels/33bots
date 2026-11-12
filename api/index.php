<?php
/**
 * Publiczne API 33bots i serwer MCP — jeden plik, bez zależności.
 *
 *   GET  /api/             opis API (JSON)
 *   GET  /api/wycena       orientacyjna cena: ?rynek=pl|de|at|lt&dni=1..30&krotki=1
 *   POST /api/zapytania    zapytanie o termin i wycenę (JSON) → ten sam formularz co na stronie
 *   POST /mcp              serwer MCP (Streamable HTTP, bez sesji): get_offer_info, get_quote, request_quote
 *
 * Ceny i zasady są te same co na stronach 33bots.pl / .de / .at / .lt (pełny dzień „od”, −15% na każdy
 * dzień od dwóch dni, krótszy pokaz wyceniany indywidualnie). Zmiana ceny na stronie = zmiana tutaj.
 *
 * Zapytanie trafia do tego samego odbiorcy co formularz na stronie (te same nazwy pól), więc w CRM
 * wygląda jak zgłoszenie ze strony z dopiskiem, że przyszło przez API. Nic nie zapisujemy na dysku
 * poza licznikami ograniczenia liczby zgłoszeń (znaczniki czasu pod skrótem adresu IP).
 */
declare(strict_types=1);

if (!function_exists('mb_substr')) {   // hosting bez rozszerzenia mbstring
    function mb_substr($t, $od, $ile) { return substr($t, $od, $ile); }
    function mb_strlen($t) { return strlen($t); }
}

const WERSJA = '1.0.0';
const ODBIORCA = 'https://formspree.io/f/mnjwvray';     // ten sam adres co formularz na stronie
const LIMIT_NA_GODZINE = 5;                              // zapytań z jednego adresu IP
const LIMIT_NA_DOBE = 60;                                // zapytań łącznie
const MAKS_CIALO = 16384;                                // bajtów w żądaniu
const WERSJE_MCP = ['2025-06-18', '2025-03-26', '2024-11-05'];

const RYNKI = [
    'pl' => [
        'kraj' => 'Polska', 'jezyk' => 'pl', 'strona' => 'https://33bots.pl/', 'mail' => 'kontakt@33bots.pl',
        'dzien' => 5500, 'waluta' => 'PLN', 'podatek' => 'netto',
        'w_cenie' => ['operator', 'transport', 'branding (logo, kod QR)', 'ubezpieczenie OC'],
    ],
    'de' => [
        'kraj' => 'Deutschland', 'jezyk' => 'de', 'strona' => 'https://33bots.de/', 'mail' => 'kontakt@33bots.de',
        'dzien' => 2500, 'waluta' => 'EUR', 'podatek' => null,
        'w_cenie' => ['Operator', 'Anfahrt deutschlandweit', 'Branding (Logo, QR-Code)', 'Haftpflichtversicherung'],
    ],
    'at' => [
        'kraj' => 'Österreich', 'jezyk' => 'de', 'strona' => 'https://33bots.at/', 'mail' => 'kontakt@33bots.at',
        'dzien' => 2300, 'waluta' => 'EUR', 'podatek' => 'netto',
        'w_cenie' => ['Operator', 'Transport in ganz Österreich', 'Branding (Logo, QR-Code)', 'Haftpflichtversicherung'],
    ],
    'lt' => [
        'kraj' => 'Lietuva', 'jezyk' => 'lt', 'strona' => 'https://33bots.lt/', 'mail' => 'kontakt@33bots.lt',
        'dzien' => 2100, 'waluta' => 'EUR', 'podatek' => 'be PVM',
        'w_cenie' => ['operatorius', 'atvykimas', 'prekės ženklo pateikimas (logotipas, QR kodas)', 'civilinės atsakomybės draudimas'],
    ],
];
const RABAT_OD_DWOCH_DNI = 0.15;
const TELEFON = '+48 531 408 004';

// ───────────────────────── wspólne ─────────────────────────

function odpowiedz(int $kod, ?array $dane, array $naglowki = []): void
{
    http_response_code($kod);
    header('Content-Type: application/json; charset=utf-8');
    header('X-Robots-Tag: noindex');
    header('Access-Control-Allow-Origin: *');
    foreach ($naglowki as $n => $w) {
        header("$n: $w");
    }
    if ($dane !== null) {
        echo json_encode($dane, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT);
    }
    exit;
}

function blad(int $kod, string $kod_bledu, string $opis, array $naglowki = []): void
{
    odpowiedz($kod, ['blad' => $kod_bledu, 'opis' => $opis], ['Cache-Control' => 'no-store'] + $naglowki);
}

function tekst($w, int $maks): string
{
    if (!is_string($w) && !is_int($w) && !is_float($w)) {
        return '';
    }
    $t = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', (string) $w) ?? '';
    return mb_substr(trim($t), 0, $maks);
}

function cialo_json(): array
{
    $surowe = file_get_contents('php://input', false, null, 0, MAKS_CIALO + 1);
    if ($surowe === false || strlen($surowe) > MAKS_CIALO) {
        blad(413, 'za_duze', 'Żądanie jest za duże (limit 16 kB).');
    }
    $dane = json_decode($surowe, true);
    if (!is_array($dane)) {
        blad(400, 'zly_json', 'Treść żądania musi być poprawnym JSON-em (Content-Type: application/json).');
    }
    return $dane;
}

// ───────────────────────── wycena ─────────────────────────

function wycena(string $rynek, int $dni, bool $krotki): array
{
    $r = RYNKI[$rynek];
    $podatek = $r['podatek'] ? ' ' . $r['podatek'] : '';
    $wynik = [
        'rynek' => $rynek, 'kraj' => $r['kraj'], 'waluta' => $r['waluta'],
        'cena_za_dzien_od' => $r['dzien'], 'podatek' => $r['podatek'],
        'w_cenie' => $r['w_cenie'],
        'zaliczka' => false, 'platnosc' => 'faktura po wydarzeniu',
        'strona' => $r['strona'], 'kontakt' => ['telefon' => TELEFON, 'email' => $r['mail']],
    ];
    if ($krotki) {
        $wynik += [
            'format' => 'krótki pokaz (kilka godzin)', 'kwota_od' => null,
            'opis' => 'Krótszy pokaz wyceniamy indywidualnie, zawsze taniej niż pełny dzień (' . $r['dzien'] . ' ' . $r['waluta'] . $podatek . ').',
        ];
    } else {
        $rabat = $dni >= 2 ? RABAT_OD_DWOCH_DNI : 0.0;
        $kwota = (int) round($dni * $r['dzien'] * (1 - $rabat));
        $wynik += [
            'format' => $dni === 1 ? 'pełny dzień' : "$dni dni", 'dni' => $dni,
            'rabat_procent' => (int) round($rabat * 100), 'kwota_od' => $kwota,
            'opis' => 'Od ' . number_format($kwota, 0, ',', ' ') . ' ' . $r['waluta'] . $podatek
                . ($dni >= 2 ? " za $dni dni (rabat 15% na każdy dzień)." : ' za pełny dzień wydarzenia.'),
        ];
    }
    $wynik['uwaga'] = 'Kwota orientacyjna „od”. Ostateczną cenę podajemy po krótkiej rozmowie o programie i miejscu, zwykle w ciągu 30 minut.';
    return $wynik;
}

function parametry_wyceny(array $zrodlo): array
{
    $rynek = strtolower(tekst($zrodlo['rynek'] ?? 'pl', 4)) ?: 'pl';
    if (!isset(RYNKI[$rynek])) {
        return ['blad' => 'Nieznany rynek. Dozwolone: pl, de, at, lt.'];
    }
    $dni = filter_var($zrodlo['dni'] ?? 1, FILTER_VALIDATE_INT);
    if ($dni === false || $dni < 1 || $dni > 30) {
        return ['blad' => 'Liczba dni musi być liczbą całkowitą od 1 do 30.'];
    }
    $krotki = filter_var($zrodlo['krotki'] ?? false, FILTER_VALIDATE_BOOLEAN);
    return ['rynek' => $rynek, 'dni' => $dni, 'krotki' => $krotki];
}

// ───────────────────────── zapytanie ─────────────────────────

function sprawdz_zapytanie(array $d): array
{
    $bledy = [];
    $z = [
        'imie' => tekst($d['imie'] ?? $d['name'] ?? '', 120),
        'email' => tekst($d['email'] ?? '', 160),
        'telefon' => tekst($d['telefon'] ?? $d['phone'] ?? '', 40),
        'firma' => tekst($d['firma'] ?? $d['company'] ?? '', 160),
        'data' => tekst($d['data'] ?? $d['date'] ?? '', 20),
        'miejsce' => tekst($d['miejsce'] ?? $d['location'] ?? '', 200),
        'rodzaj' => tekst($d['rodzaj'] ?? $d['event_type'] ?? '', 60),
        'goscie' => tekst($d['goscie'] ?? $d['guests'] ?? '', 30),
        'opis' => tekst($d['opis'] ?? $d['message'] ?? '', 3000),
        'rynek' => strtolower(tekst($d['rynek'] ?? 'pl', 4)) ?: 'pl',
    ];
    if (mb_strlen($z['imie']) < 2) {
        $bledy['imie'] = 'Podaj imię i nazwisko osoby kontaktowej.';
    }
    if (!filter_var($z['email'], FILTER_VALIDATE_EMAIL)) {
        $bledy['email'] = 'Podaj poprawny adres e-mail, na który mamy odpowiedzieć.';
    }
    if ($z['telefon'] !== '' && !preg_match('/^[0-9 +()\-]{6,40}$/', $z['telefon'])) {
        $bledy['telefon'] = 'Numer telefonu może zawierać cyfry, spacje, +, - i nawiasy.';
    }
    if (!isset(RYNKI[$z['rynek']])) {
        $bledy['rynek'] = 'Dozwolone rynki: pl, de, at, lt.';
    }
    if ($z['data'] !== '' && $z['data'] !== 'nieustalony') {
        $dt = DateTimeImmutable::createFromFormat('!Y-m-d', $z['data']);
        if (!$dt || $dt->format('Y-m-d') !== $z['data']) {
            $bledy['data'] = 'Data w formacie RRRR-MM-DD albo „nieustalony”.';
        } elseif ($dt < new DateTimeImmutable('yesterday')) {
            $bledy['data'] = 'Data wydarzenia nie może być w przeszłości.';
        }
    }
    if (($d['zgoda'] ?? false) !== true) {
        $bledy['zgoda'] = 'Ustaw "zgoda": true — potwierdzenie, że osoba, której dane przesyłasz, chce, żeby 33bots się z nią skontaktowało.';
    }
    if (preg_match_all('~https?://~i', $z['opis']) > 3) {
        $bledy['opis'] = 'Za dużo odnośników w opisie.';
    }
    return [$z, $bledy];
}

/** Ograniczenie liczby zgłoszeń: znaczniki czasu w katalogu tymczasowym, bez danych osobowych. */
function limit_przekroczony(): bool
{
    $kat = sys_get_temp_dir() . '/33bots_api';
    if (!is_dir($kat) && !@mkdir($kat, 0700, true) && !is_dir($kat)) {
        return false;   // brak miejsca na liczniki nie może blokować prawdziwych zapytań
    }
    $teraz = time();
    $ip = hash('sha256', 'limit|' . ($_SERVER['REMOTE_ADDR'] ?? ''));
    $progi = ["$kat/ip_$ip" => [3600, LIMIT_NA_GODZINE], "$kat/doba" => [86400, LIMIT_NA_DOBE]];
    $stany = [];
    foreach ($progi as $plik => [$okno, $limit]) {
        $czasy = array_filter(array_map('intval', @file($plik, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) ?: []),
            fn (int $t) => $t > $teraz - $okno);
        if (count($czasy) >= $limit) {
            return true;
        }
        $stany[$plik] = $czasy;
    }
    foreach ($stany as $plik => $czasy) {
        $czasy[] = $teraz;
        @file_put_contents($plik, implode("\n", $czasy) . "\n", LOCK_EX);
    }
    return false;
}

/** Przekazuje zapytanie do odbiorcy formularza. Zwraca [czy_przyjęte, kod_http]. */
function przekaz(array $z, string $kanal): array
{
    $r = RYNKI[$z['rynek']];
    $pola = [
        'name' => $z['imie'],
        'company' => $z['firma'] ?: '—',
        'email' => $z['email'],
        'phone' => $z['telefon'] ?: '—',
        'date' => $z['data'] ?: '—',
        'location' => $z['miejsce'] ?: '—',
        'message' => "[Zgłoszenie przez $kanal · rynek: {$r['kraj']}]\n" . ($z['opis'] ?: '—'),
        'event_type' => $z['rodzaj'] ?: '—',
        'guests' => $z['goscie'] ?: '—',
    ];
    $adres = getenv('API_33BOTS_ODBIORCA') ?: ODBIORCA;
    $tresc = json_encode($pola, JSON_UNESCAPED_UNICODE);
    $naglowki = ['Content-Type: application/json', 'Accept: application/json',
        'Origin: https://33bots.pl', 'Referer: https://33bots.pl/api/zapytania'];
    $odp = false;
    $kod = 0;
    if (function_exists('curl_init')) {
        // Ta sama droga co w deploy.php: na hostingu współdzielonym curl działa także wtedy,
        // gdy allow_url_fopen jest wyłączone.
        $ch = curl_init($adres);
        curl_setopt_array($ch, [
            CURLOPT_POST => true, CURLOPT_POSTFIELDS => $tresc, CURLOPT_HTTPHEADER => $naglowki,
            CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 15, CURLOPT_CONNECTTIMEOUT => 8,
            CURLOPT_USERAGENT => '33bots-api/' . WERSJA,
        ]);
        $odp = curl_exec($ch);
        $kod = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
        curl_close($ch);
    } else {
        $kontekst = stream_context_create(['http' => [
            'method' => 'POST', 'timeout' => 15, 'ignore_errors' => true,
            'header' => implode("\r\n", $naglowki) . "\r\nUser-Agent: 33bots-api/" . WERSJA . "\r\n",
            'content' => $tresc,
        ]]);
        $odp = @file_get_contents($adres, false, $kontekst);
        foreach ($http_response_header ?? [] as $linia) {
            if (preg_match('~^HTTP/\S+\s+(\d{3})~', $linia, $m)) {
                $kod = (int) $m[1];
            }
        }
    }
    return [$odp !== false && $kod >= 200 && $kod < 300, $kod];
}

/** Pełna obsługa zapytania. Zwraca [kod_http, tablica_odpowiedzi]. */
function przyjmij_zapytanie(array $d, string $kanal): array
{
    [$z, $bledy] = sprawdz_zapytanie($d);
    if ($bledy) {
        return [422, ['blad' => 'niepoprawne_dane', 'opis' => 'Popraw wskazane pola i wyślij ponownie.', 'pola' => $bledy]];
    }
    $r = RYNKI[$z['rynek']];
    $ok = [
        'status' => 'przyjete',
        'opis' => 'Zapytanie trafiło do 33bots. Odpowiadamy zwykle w ciągu 30 minut na podany adres e-mail; wycenę od razu podajemy przez telefon.',
        'kontakt' => ['telefon' => TELEFON, 'email' => $r['mail']],
    ];
    if (tekst($d['website'] ?? '', 50) !== '') {
        return [201, $ok];   // pole-pułapka: automat dostaje „przyjęte”, nic nie przekazujemy
    }
    if (limit_przekroczony()) {
        return [429, ['blad' => 'za_duzo_zapytan', 'opis' => 'Za dużo zapytań z tego adresu. Spróbuj za godzinę albo zadzwoń: ' . TELEFON . '.']];
    }
    [$przyjete, $kod] = przekaz($z, $kanal);
    if (!$przyjete) {
        return [502, ['blad' => 'nie_przekazano', 'opis' => 'Nie udało się przekazać zapytania. Zadzwoń: ' . TELEFON . ' albo napisz: ' . $r['mail'] . '.', 'kod_odbiorcy' => $kod]];
    }
    return [201, $ok];
}

// ───────────────────────── informacje ─────────────────────────

function informacje(): array
{
    $ceny = [];
    foreach (RYNKI as $kod => $r) {
        $ceny[$kod] = ['kraj' => $r['kraj'], 'pelny_dzien_od' => $r['dzien'], 'waluta' => $r['waluta'], 'podatek' => $r['podatek'],
            'w_cenie' => $r['w_cenie'], 'strona' => $r['strona'], 'email' => $r['mail']];
    }
    return [
        'firma' => '33bots — wynajem robota humanoidalnego Unitree G1 na wydarzenia',
        'robot' => 'Unitree G1: 132 cm, ok. 35 kg, 23 stopnie swobody. Chodzi, gestykuluje, wita gości, pozuje do zdjęć, tańczy i rozmawia w języku wydarzenia.',
        'jak_pracuje' => 'Zawsze z operatorem 33bots, według scenariusza ustalonego z organizatorem. Przed wydarzeniem wgrywamy informacje o wydarzeniu, firmie, ofercie i najczęstszych pytaniach gości.',
        'wymagania' => 'Równa powierzchnia ok. 2×2 m i zwykłe gniazdko 230 V. Wymienne baterie — pokaz nie zatrzymuje się na ładowanie. Na zewnątrz tylko na suchej, równej nawierzchni.',
        'ceny' => $ceny,
        'zasady' => [
            'rabat' => '15% na każdy dzień przy realizacjach od dwóch dni',
            'krotki_pokaz' => 'kilka godzin — wycena indywidualna, zawsze taniej niż pełny dzień',
            'zaliczka' => 'bez zaliczki, faktura po wydarzeniu',
            'odpowiedz' => 'zwykle w ciągu 30 minut, przez telefon od razu',
        ],
        'kontakt' => ['telefon' => TELEFON, 'email' => 'kontakt@33bots.pl'],
        'prywatnosc' => 'https://33bots.pl/polityka-prywatnosci.html',
    ];
}

function opis_api(): array
{
    return [
        'nazwa' => 'API 33bots', 'wersja' => WERSJA,
        'opis' => 'Orientacyjna cena i zapytanie o termin wynajmu robota humanoidalnego Unitree G1 na wydarzenie. Bez klucza.',
        'zasoby' => [
            'GET /api/wycena' => 'orientacyjna cena; parametry: rynek (pl|de|at|lt), dni (1–30), krotki (1 = kilka godzin)',
            'POST /api/zapytania' => 'zapytanie o termin i wycenę (JSON); wymagane: imie, email, zgoda=true; opcjonalne: telefon, firma, data (RRRR-MM-DD albo „nieustalony”), miejsce, rodzaj, goscie, opis, rynek',
            'POST /mcp' => 'serwer MCP (Streamable HTTP): narzędzia get_offer_info, get_quote, request_quote',
        ],
        'specyfikacja' => 'https://33bots.pl/api/openapi.json',
        'limity' => LIMIT_NA_GODZINE . ' zapytań na godzinę z jednego adresu IP',
        'informacje' => informacje(),
    ];
}

// ───────────────────────── MCP ─────────────────────────

function narzedzia_mcp(): array
{
    $rynek = ['type' => 'string', 'enum' => array_keys(RYNKI), 'default' => 'pl',
        'description' => 'Kraj wydarzenia / event country: pl = Polska, de = Deutschland, at = Österreich, lt = Lietuva'];
    return [
        [
            'name' => 'get_offer_info',
            'title' => 'Oferta 33bots',
            'description' => 'Informacje o wynajmie robota humanoidalnego Unitree G1 od 33bots: co robot robi na wydarzeniu, co jest w cenie, wymagania techniczne, ceny „od” dla Polski, Niemiec, Austrii i Litwy, kontakt. / Facts about renting the Unitree G1 humanoid robot for events from 33bots.',
            'inputSchema' => ['type' => 'object', 'properties' => new stdClass(), 'additionalProperties' => false],
            'annotations' => ['readOnlyHint' => true, 'openWorldHint' => false],
        ],
        [
            'name' => 'get_quote',
            'title' => 'Orientacyjna cena',
            'description' => 'Orientacyjna cena „od” za wynajem robota: pełny dzień albo kilka dni (rabat 15% na każdy dzień od dwóch dni). Krótszy pokaz jest wyceniany indywidualnie. / Starting price for a full event day or several days.',
            'inputSchema' => ['type' => 'object', 'properties' => [
                'rynek' => $rynek,
                'dni' => ['type' => 'integer', 'minimum' => 1, 'maximum' => 30, 'default' => 1, 'description' => 'Liczba dni wydarzenia / number of event days'],
                'krotki' => ['type' => 'boolean', 'default' => false, 'description' => 'true = krótki pokaz na kilka godzin / short show of a few hours'],
            ], 'additionalProperties' => false],
            'annotations' => ['readOnlyHint' => true, 'openWorldHint' => false],
        ],
        [
            'name' => 'request_quote',
            'title' => 'Zapytanie o termin i wycenę',
            'description' => 'Wysyła do 33bots zapytanie o termin i wycenę w imieniu użytkownika. 33bots odpowiada zwykle w ciągu 30 minut na podany e-mail. Wywołuj wyłącznie wtedy, gdy użytkownik sam podał swoje dane kontaktowe i wyraźnie potwierdził, że chce wysłać zapytanie; nie wymyślaj żadnych danych. / Sends a booking inquiry to 33bots on the user\'s behalf. Call only after the user has provided their own contact details and explicitly confirmed sending.',
            'inputSchema' => ['type' => 'object', 'required' => ['imie', 'email', 'zgoda'], 'properties' => [
                'imie' => ['type' => 'string', 'description' => 'Imię i nazwisko osoby kontaktowej / contact person'],
                'email' => ['type' => 'string', 'format' => 'email', 'description' => 'Adres e-mail do odpowiedzi / reply e-mail'],
                'telefon' => ['type' => 'string', 'description' => 'Telefon (opcjonalnie)'],
                'firma' => ['type' => 'string', 'description' => 'Firma lub organizator (opcjonalnie)'],
                'data' => ['type' => 'string', 'description' => 'Data wydarzenia RRRR-MM-DD albo „nieustalony”'],
                'miejsce' => ['type' => 'string', 'description' => 'Miasto i miejsce wydarzenia'],
                'rodzaj' => ['type' => 'string', 'description' => 'Rodzaj wydarzenia: gala, konferencja, targi, plener, inne'],
                'goscie' => ['type' => 'string', 'description' => 'Przybliżona liczba gości'],
                'opis' => ['type' => 'string', 'description' => 'Czego oczekuje organizator: rola robota, liczba dni, pytania'],
                'rynek' => $rynek,
                'zgoda' => ['type' => 'boolean', 'description' => 'true tylko wtedy, gdy użytkownik potwierdził, że chce przekazać swoje dane 33bots w celu odpowiedzi na zapytanie'],
            ], 'additionalProperties' => false],
            'annotations' => ['readOnlyHint' => false, 'destructiveHint' => false, 'idempotentHint' => false, 'openWorldHint' => true],
        ],
    ];
}

function wynik_mcp(array $dane, string $tekst, bool $blad = false): array
{
    return ['content' => [['type' => 'text', 'text' => $tekst]], 'structuredContent' => $dane, 'isError' => $blad];
}

function wywolaj_mcp(string $nazwa, array $arg): array
{
    if ($nazwa === 'get_offer_info') {
        $i = informacje();
        return wynik_mcp($i, json_encode($i, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT));
    }
    if ($nazwa === 'get_quote') {
        $p = parametry_wyceny($arg);
        if (isset($p['blad'])) {
            return wynik_mcp(['blad' => $p['blad']], $p['blad'], true);
        }
        $w = wycena($p['rynek'], $p['dni'], $p['krotki']);
        return wynik_mcp($w, $w['opis'] . ' W cenie: ' . implode(', ', $w['w_cenie']) . '. ' . $w['uwaga']);
    }
    if ($nazwa === 'request_quote') {
        [$kod, $odp] = przyjmij_zapytanie($arg, 'asystenta AI (MCP)');
        $tekst = $odp['opis'] . (isset($odp['pola']) ? ' ' . implode(' ', $odp['pola']) : '');
        return wynik_mcp($odp, $tekst, $kod >= 400);
    }
    return wynik_mcp(['blad' => 'nieznane_narzedzie'], "Nieznane narzędzie: $nazwa", true);
}

/** Jedna wiadomość JSON-RPC. Zwraca odpowiedź albo null (powiadomienie). */
function obsluz_mcp($w): ?array
{
    if (!is_array($w) || ($w['jsonrpc'] ?? '') !== '2.0' || !is_string($w['method'] ?? null)) {
        return ['jsonrpc' => '2.0', 'id' => is_array($w) ? ($w['id'] ?? null) : null,
            'error' => ['code' => -32600, 'message' => 'Invalid Request']];
    }
    if (!array_key_exists('id', $w)) {
        return null;   // powiadomienie (np. notifications/initialized)
    }
    $id = $w['id'];
    $p = is_array($w['params'] ?? null) ? $w['params'] : [];
    switch ($w['method']) {
        case 'initialize':
            $wynik = [
                'protocolVersion' => in_array($p['protocolVersion'] ?? '', WERSJE_MCP, true) ? $p['protocolVersion'] : WERSJE_MCP[0],
                'capabilities' => ['tools' => ['listChanged' => false]],
                'serverInfo' => ['name' => '33bots', 'title' => '33bots — wynajem robota humanoidalnego', 'version' => WERSJA],
                'instructions' => 'Serwer 33bots: wynajem robota humanoidalnego Unitree G1 na wydarzenia w Polsce, Niemczech, Austrii i na Litwie. get_offer_info i get_quote tylko czytają. request_quote wysyła prawdziwe zapytanie do firmy — używaj go dopiero po wyraźnej zgodzie użytkownika i tylko z danymi, które sam podał.',
            ];
            break;
        case 'ping':
            $wynik = new stdClass();
            break;
        case 'tools/list':
            $wynik = ['tools' => narzedzia_mcp()];
            break;
        case 'tools/call':
            $wynik = is_string($p['name'] ?? null)
                ? wywolaj_mcp($p['name'], is_array($p['arguments'] ?? null) ? $p['arguments'] : [])
                : null;
            break;
        default:
            $wynik = false;
    }
    if ($wynik === false) {
        return ['jsonrpc' => '2.0', 'id' => $id, 'error' => ['code' => -32601, 'message' => 'Method not found']];
    }
    if ($wynik === null) {
        return ['jsonrpc' => '2.0', 'id' => $id, 'error' => ['code' => -32602, 'message' => 'Invalid params: name']];
    }
    return ['jsonrpc' => '2.0', 'id' => $id, 'result' => $wynik];
}

// ───────────────────────── trasy ─────────────────────────

$metoda = $_SERVER['REQUEST_METHOD'] ?? 'GET';
$zasob = tekst($_GET['zasob'] ?? '', 20);

if ($metoda === 'OPTIONS') {
    header('Access-Control-Allow-Origin: *');
    header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
    header('Access-Control-Allow-Headers: Content-Type, Accept, Mcp-Session-Id, MCP-Protocol-Version');
    header('Access-Control-Max-Age: 86400');
    http_response_code(204);
    exit;
}

if ($zasob === 'mcp') {
    if ($metoda !== 'POST') {
        blad(405, 'tylko_post', 'Serwer MCP przyjmuje wiadomości JSON-RPC metodą POST. Opis: https://33bots.pl/api/', ['Allow' => 'POST, OPTIONS']);
    }
    $wiad = cialo_json();
    $lista = $wiad === [] || array_keys($wiad) === range(0, count($wiad) - 1);
    $odp = array_values(array_filter(array_map('obsluz_mcp', $lista ? $wiad : [$wiad]), fn ($o) => $o !== null));
    if (!$odp) {
        http_response_code(202);   // same powiadomienia
        header('Access-Control-Allow-Origin: *');
        exit;
    }
    odpowiedz(200, $lista ? $odp : $odp[0], ['Cache-Control' => 'no-store']);
}

if ($zasob === 'wycena') {
    if ($metoda !== 'GET') {
        blad(405, 'tylko_get', 'Wycena jest dostępna metodą GET.', ['Allow' => 'GET, OPTIONS']);
    }
    $p = parametry_wyceny($_GET);
    if (isset($p['blad'])) {
        blad(422, 'niepoprawne_dane', $p['blad']);
    }
    odpowiedz(200, wycena($p['rynek'], $p['dni'], $p['krotki']), ['Cache-Control' => 'public, max-age=300']);
}

if ($zasob === 'zapytania') {
    if ($metoda !== 'POST') {
        blad(405, 'tylko_post', 'Zapytanie wysyła się metodą POST z treścią JSON. Opis pól: https://33bots.pl/api/', ['Allow' => 'POST, OPTIONS']);
    }
    [$kod, $odp] = przyjmij_zapytanie(cialo_json(), 'API');
    odpowiedz($kod, $odp, ['Cache-Control' => 'no-store']);
}

if ($zasob === '') {
    odpowiedz(200, opis_api(), ['Cache-Control' => 'public, max-age=300']);
}

blad(404, 'nie_ma', 'Nie ma takiego zasobu. Opis API: https://33bots.pl/api/');
