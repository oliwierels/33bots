<?php
// Router dla wbudowanego serwera PHP — odwzorowuje reguły z .htaccess (tylko do testów lokalnych).
$sciezka = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
if (preg_match('~^/api/?$~', $sciezka)) { $_GET['zasob'] = ''; }
elseif (is_file(__DIR__ . '/../..' . $sciezka)) { return false; }   // np. /api/openapi.json
elseif (preg_match('~^/api/([a-z0-9-]+)/?$~', $sciezka, $m)) { $_GET['zasob'] = $m[1]; }
elseif (preg_match('~^/mcp/?$~', $sciezka)) { $_GET['zasob'] = 'mcp'; }
else { return false; }
require __DIR__ . '/../../api/index.php';
