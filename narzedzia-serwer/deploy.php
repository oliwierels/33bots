<?php
/**
 * 33bots — punkt wdrożeniowy po stronie serwera.
 *
 * Pobiera aktualną wersję strony z GitHuba po HTTPS i rozpakowuje ją
 * do katalogu, w którym leży ten plik. Kierunek jest odwrotny niż przy
 * FTP: to serwer sięga po zmiany, dzięki czemu nie trzeba wpuszczać
 * niczego z zewnątrz ani przechowywać hasła FTP poza hostingiem.
 *
 * INSTALACJA
 *   1. Wpisz własny token w stałej TOKEN poniżej (ten sam, co w sekrecie
 *      DEPLOY_TOKEN w repozytorium na GitHubie).
 *   2. Wgraj ten plik do public_html domeny 33bots.pl.
 *   3. Sprawdź w przeglądarce:
 *      https://33bots.pl/deploy.php?token=TWOJ_TOKEN&test=1
 *
 * Bez poprawnego tokenu skrypt nie robi nic i zwraca 403.
 */

declare(strict_types=1);

// ─────────────────────────────────────────────────────────────
//  KONFIGURACJA
// ─────────────────────────────────────────────────────────────

const TOKEN     = 'WSTAW_TUTAJ_SWOJ_TOKEN';
const REPO      = 'oliwierels/33bots';
const GALAZ     = 'claude/33bots-website-T0REs';
const KATALOG   = __DIR__;          // gdzie lądują pliki strony
const LIMIT_MB  = 200;              // bezpiecznik na rozmiar pobrania

/** Czego nie nadpisujemy na serwerze — narzędzia i materiały źródłowe. */
const POMIJANE_KATALOGI = ['.git', '.github', 'node_modules', '__pycache__', 'og', 'scripts', 'narzedzia-serwer'];
const POMIJANE_PLIKI    = ['.gitignore', '.deployignore', '_redirects', 'szablon-case-study.html', 'deploy.php'];
const POMIJANE_KONCOWKI = ['.py', '.md', '.HEIC', '.DNG'];
const POMIJANE_NAZWY    = ['tailwind.config.js', 'tw-input.css', 'package.json', 'package-lock.json', 'buduj.sh'];

// ─────────────────────────────────────────────────────────────

set_time_limit(600);
ignore_user_abort(true);
header('Content-Type: text/plain; charset=utf-8');

$podany = $_GET['token'] ?? $_POST['token'] ?? '';

// Sprawdzamy długość, a nie zgodność z konkretnym napisem — dzięki temu
// podmiana placeholdera zwykłym „znajdź i zamień" nie uszkodzi zabezpieczenia.
if (strlen(TOKEN) < 16) {
    http_response_code(500);
    exit("Skrypt nie został skonfigurowany — wpisz własny token w stałej TOKEN.\n");
}
if (!is_string($podany) || !hash_equals(TOKEN, $podany)) {
    http_response_code(403);
    exit("Brak dostępu.\n");
}

$start = microtime(true);
$log = static function (string $tekst): void {
    echo $tekst . "\n";
    if (ob_get_level() > 0) { ob_flush(); }
    flush();
};

// Tryb testowy — sprawdza gotowość środowiska, niczego nie zmienia.
if (isset($_GET['test'])) {
    $log('Token poprawny.');
    $log('PHP: ' . PHP_VERSION);
    $log('ZipArchive: ' . (class_exists('ZipArchive') ? 'dostępny' : 'BRAK — wdrożenie się nie uda'));
    $log('cURL: ' . (function_exists('curl_init') ? 'dostępny' : 'BRAK'));
    $log('Katalog docelowy: ' . KATALOG);
    $log('Zapis do katalogu: ' . (is_writable(KATALOG) ? 'możliwy' : 'ZABLOKOWANY — sprawdź uprawnienia'));
    $log('Katalog tymczasowy: ' . sys_get_temp_dir() . (is_writable(sys_get_temp_dir()) ? ' (zapisywalny)' : ' (BRAK ZAPISU)'));
    exit;
}

if (!class_exists('ZipArchive')) {
    http_response_code(500);
    exit("Brak rozszerzenia ZipArchive — bez niego nie rozpakuję paczki.\n");
}

/** Czy plik o tej ścieżce względnej ma trafić na serwer. */
function czyPomijac(string $sciezka): bool
{
    $czesci = explode('/', $sciezka);
    foreach ($czesci as $czesc) {
        if (in_array($czesc, POMIJANE_KATALOGI, true)) return true;
    }
    $nazwa = basename($sciezka);
    if (in_array($nazwa, POMIJANE_PLIKI, true)) return true;
    if (in_array($nazwa, POMIJANE_NAZWY, true)) return true;
    foreach (POMIJANE_KONCOWKI as $koncowka) {
        if (str_ends_with($nazwa, $koncowka)) return true;
    }
    if (preg_match('/^IMG_\d+\.(JPG|PNG|HEIC|DNG)$/i', $nazwa)) return true;
    return false;
}

function usunKatalog(string $sciezka): void
{
    if (!is_dir($sciezka)) { @unlink($sciezka); return; }
    foreach (scandir($sciezka) ?: [] as $wpis) {
        if ($wpis === '.' || $wpis === '..') continue;
        usunKatalog($sciezka . '/' . $wpis);
    }
    @rmdir($sciezka);
}

// ── 1. Pobranie paczki z GitHuba ──
$adres = sprintf('https://codeload.github.com/%s/zip/refs/heads/%s', REPO, GALAZ);
$plikZip = tempnam(sys_get_temp_dir(), '33bots_') ?: sys_get_temp_dir() . '/33bots.zip';

$log('Pobieram wersję z gałęzi ' . GALAZ . '…');

$uchwyt = fopen($plikZip, 'wb');
if ($uchwyt === false) {
    http_response_code(500);
    exit("Nie mogę utworzyć pliku tymczasowego.\n");
}

$ch = curl_init($adres);
curl_setopt_array($ch, [
    CURLOPT_FILE           => $uchwyt,
    CURLOPT_FOLLOWLOCATION => true,
    CURLOPT_MAXREDIRS      => 5,
    CURLOPT_TIMEOUT        => 300,
    CURLOPT_CONNECTTIMEOUT => 30,
    CURLOPT_USERAGENT      => '33bots-deploy',
    CURLOPT_FAILONERROR    => true,
]);
$ok = curl_exec($ch);
$blad = curl_error($ch);
$kod = (int) curl_getinfo($ch, CURLINFO_RESPONSE_CODE);
curl_close($ch);
fclose($uchwyt);

if ($ok === false) {
    @unlink($plikZip);
    http_response_code(502);
    exit("Pobieranie nie powiodło się (HTTP $kod): $blad\n");
}

$rozmiarMB = round(filesize($plikZip) / 1048576, 1);
if ($rozmiarMB > LIMIT_MB) {
    @unlink($plikZip);
    http_response_code(500);
    exit("Paczka waży {$rozmiarMB} MB — powyżej ustawionego limitu.\n");
}
$log("Pobrano {$rozmiarMB} MB.");

// ── 2. Rozpakowanie do katalogu tymczasowego ──
$tymczasowy = sys_get_temp_dir() . '/33bots_rozpakowane_' . bin2hex(random_bytes(4));
@mkdir($tymczasowy, 0755, true);

$zip = new ZipArchive();
if ($zip->open($plikZip) !== true) {
    @unlink($plikZip);
    usunKatalog($tymczasowy);
    http_response_code(500);
    exit("Nie mogę otworzyć pobranej paczki.\n");
}
$zip->extractTo($tymczasowy);
$zip->close();
@unlink($plikZip);

// GitHub pakuje zawartość w jeden katalog nadrzędny — wchodzimy do niego.
$zrodlo = null;
foreach (scandir($tymczasowy) ?: [] as $wpis) {
    if ($wpis !== '.' && $wpis !== '..' && is_dir($tymczasowy . '/' . $wpis)) {
        $zrodlo = $tymczasowy . '/' . $wpis;
        break;
    }
}
if ($zrodlo === null) {
    usunKatalog($tymczasowy);
    http_response_code(500);
    exit("Paczka ma nieoczekiwaną strukturę.\n");
}

// ── 3. Przeniesienie plików na stronę ──
$skopiowane = 0;
$pominiete  = 0;
$bezZmian   = 0;

$iterator = new RecursiveIteratorIterator(
    new RecursiveDirectoryIterator($zrodlo, FilesystemIterator::SKIP_DOTS),
    RecursiveIteratorIterator::SELF_FIRST
);

foreach ($iterator as $element) {
    /** @var SplFileInfo $element */
    $wzgledna = ltrim(str_replace('\\', '/', substr($element->getPathname(), strlen($zrodlo))), '/');
    if ($wzgledna === '') continue;

    if (czyPomijac($wzgledna)) { $pominiete++; continue; }

    $cel = KATALOG . '/' . $wzgledna;

    if ($element->isDir()) {
        if (!is_dir($cel)) @mkdir($cel, 0755, true);
        continue;
    }

    // nie ruszamy pliku, jeśli treść jest identyczna
    if (is_file($cel) && filesize($cel) === $element->getSize()
        && md5_file($cel) === md5_file($element->getPathname())) {
        $bezZmian++;
        continue;
    }

    $katalogCelu = dirname($cel);
    if (!is_dir($katalogCelu)) @mkdir($katalogCelu, 0755, true);

    if (@copy($element->getPathname(), $cel)) {
        $skopiowane++;
    } else {
        $log('  UWAGA: nie udało się zapisać ' . $wzgledna);
    }
}

usunKatalog($tymczasowy);

$czas = round(microtime(true) - $start, 1);
$log('');
$log('=== WDROŻENIE ZAKOŃCZONE ===');
$log("Zaktualizowane pliki: {$skopiowane}");
$log("Bez zmian: {$bezZmian}");
$log("Pominięte (narzędzia i materiały źródłowe): {$pominiete}");
$log("Czas: {$czas} s");
