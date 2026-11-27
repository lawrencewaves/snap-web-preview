<?php
// SNAP · contador de visitas propio, sin cookies ni identificadores: solo día, página y origen de campaña, agregados.
declare(strict_types=1);
ini_set('display_errors', '0');   // nunca mostrar errores al visitante (rutas, versiones); van al log del servidor
http_response_code(204);
if ($_SERVER['REQUEST_METHOD'] !== 'POST') exit;
$cfg = require __DIR__ . '/config.php';
$d = json_decode((string)file_get_contents('php://input', false, null, 0, 2000), true);
if (!is_array($d)) exit;
$page = substr(preg_replace('#[^a-z0-9/_-]#i', '', (string)($d['p'] ?? '/')), 0, 120) ?: '/';
$src = substr(preg_replace('#[^a-z0-9._-]#i', '', strtolower((string)($d['s'] ?? ''))), 0, 40);
if ($src === '') {
    $ref = parse_url((string)($_SERVER['HTTP_REFERER'] ?? ''), PHP_URL_HOST) ?: '';
    $src = (string)($d['r'] ?? '') !== '' ? substr(preg_replace('#[^a-z0-9.-]#i', '', strtolower((string)parse_url((string)$d['r'], PHP_URL_HOST))), 0, 40) : 'directo';
    if ($src === strtolower((string)$ref) || $src === '') $src = 'directo';
}
if (preg_match('/bot|crawl|spider|slurp|preview/i', (string)($_SERVER['HTTP_USER_AGENT'] ?? ''))) exit;
try {
    $db = new PDO('sqlite:' . $cfg['db']);
    $db->exec('CREATE TABLE IF NOT EXISTS hits (day TEXT, page TEXT, src TEXT, n INTEGER, PRIMARY KEY(day,page,src))');
    $c = $db->prepare('SELECT COUNT(*) FROM hits WHERE day = ?'); $c->execute([gmdate('Y-m-d')]);
    if ((int)$c->fetchColumn() >= 1500) exit;   // tope diario de filas distintas (la web tiene 48 páginas)
    $db->prepare('INSERT INTO hits VALUES (?,?,?,1) ON CONFLICT(day,page,src) DO UPDATE SET n=n+1')->execute([gmdate('Y-m-d'), $page, $src ?: 'directo']);
} catch (Throwable $t) { error_log('SNAP hit: ' . $t->getMessage()); }
