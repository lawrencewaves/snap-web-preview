<?php
// SNAP · resumen de visitas (últimos 30 días). Uso: /api/stats.php?key=CRONKEY
declare(strict_types=1);
ini_set('display_errors', '0');   // nunca mostrar errores al visitante (rutas, versiones); van al log del servidor
$cfg = require __DIR__ . '/config.php';
header('Cache-Control: no-store'); header('X-Robots-Tag: noindex'); header('Referrer-Policy: no-referrer');
if (str_starts_with((string)$cfg['cronKey'], 'CAMBIAR') || !hash_equals((string)$cfg['cronKey'], (string)($_GET['key'] ?? ''))) { sleep(2); http_response_code(403); exit; }
header('Content-Type: text/plain; charset=utf-8');
$db = new PDO('sqlite:' . $cfg['db']);
$db->exec('CREATE TABLE IF NOT EXISTS hits (day TEXT, page TEXT, src TEXT, n INTEGER, PRIMARY KEY(day,page,src))');
$from = gmdate('Y-m-d', time() - 30 * 86400);
foreach (['Por origen' => 'src', 'Por página' => 'page', 'Por día' => 'day'] as $t => $c) {
    echo "== $t (30 días)\n";
    $q = $db->prepare("SELECT $c AS k, SUM(n) AS n FROM hits WHERE day >= ? GROUP BY $c ORDER BY " . ($c === 'day' ? 'k' : 'n DESC') . ' LIMIT 40');
    $q->execute([$from]);
    foreach ($q as $r) echo str_pad((string)$r['n'], 7, ' ', STR_PAD_LEFT), '  ', $r['k'], "\n";
}
// Solicitudes bloqueadas por el antispam (cuarentena de 60 días): revisar por si hubiera algún falso positivo
$db->exec('CREATE TABLE IF NOT EXISTS blocked (at TEXT, reason TEXT, ip TEXT, email TEXT, data TEXT)');
$q = $db->prepare("SELECT substr(reason, 1, instr(reason || ':', ':') - 1) AS k, COUNT(*) AS n FROM blocked WHERE at > ? GROUP BY k ORDER BY n DESC");
$q->execute([gmdate('c', time() - 30 * 86400)]);
echo "== Bloqueadas por el antispam (30 días)\n";
foreach ($q as $r) echo str_pad((string)$r['n'], 7, ' ', STR_PAD_LEFT), '  ', $r['k'], "\n";
echo "== Últimas 15 bloqueadas (fecha · motivo · email)\n";
foreach ($db->query('SELECT at, reason, email FROM blocked ORDER BY at DESC LIMIT 15') as $r) echo "{$r['at']} · {$r['reason']} · {$r['email']}\n";
