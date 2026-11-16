<?php
// SNAP SURF TRIPS · tarea diaria (cron de Dinahosting: php api/summary.php, o URL con ?key=...).
// Reenvía los emails que fallaron y manda «[WEB-ENQ-RESUMEN]» con las solicitudes de 48 h para conciliar con el CRM.
declare(strict_types=1);
$cfg = require __DIR__ . '/config.php';
if (PHP_SAPI !== 'cli' && (str_starts_with((string)$cfg['cronKey'], 'CAMBIAR') || !hash_equals((string)$cfg['cronKey'], (string)($_GET['key'] ?? '')))) { http_response_code(403); exit; }

$db = new PDO('sqlite:' . $cfg['db']);
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$h = 'From: SNAP Web <' . $cfg['from'] . ">\r\nContent-Type: text/plain; charset=utf-8";

foreach ($db->query('SELECT id, type, data FROM enquiries WHERE mail_sent = 0') as $r) {
    $s = "[WEB-ENQ] {$r['id']} · {$r['type']} (reenvío)";
    if (@mail($cfg['to'], '=?UTF-8?B?' . base64_encode($s) . '?=', json_encode(json_decode($r['data']), JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE), $h . "\r\nX-SNAP-Enquiry: {$r['id']}")) {
        $db->prepare('UPDATE enquiries SET mail_sent = 1 WHERE id = ?')->execute([$r['id']]);
    }
}
$q = $db->prepare('SELECT id, received_at, type FROM enquiries WHERE received_at > ? ORDER BY received_at');
$q->execute([gmdate('c', time() - 172800)]);
$rows = $q->fetchAll(PDO::FETCH_ASSOC);
if ($rows) {
    @mail($cfg['to'], '[WEB-ENQ-RESUMEN] ' . gmdate('Y-m-d') . ' · ' . count($rows), json_encode($rows, JSON_PRETTY_PRINT), $h);
}
echo 'ok ' . count($rows);
