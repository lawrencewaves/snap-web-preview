<?php
// SNAP · resumen de visitas (últimos 30 días). Uso: /api/stats.php?key=CRONKEY
declare(strict_types=1);
$cfg = require __DIR__ . '/config.php';
if (str_starts_with((string)$cfg['cronKey'], 'CAMBIAR') || !hash_equals((string)$cfg['cronKey'], (string)($_GET['key'] ?? ''))) { http_response_code(403); exit; }
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
