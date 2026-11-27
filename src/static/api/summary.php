<?php
// SNAP SURF TRIPS · tarea diaria (cron de Dinahosting: php api/summary.php, o URL con ?key=...).
// Reenvía los emails que fallaron y manda «[WEB-ENQ-RESUMEN]» con las solicitudes de 48 h para conciliar con el CRM.
declare(strict_types=1);
ini_set('display_errors', '0');   // nunca mostrar errores al visitante (rutas, versiones); van al log del servidor
$cfg = require __DIR__ . '/config.php';
if (isset($_SERVER['REQUEST_METHOD'])) { http_response_code(403); exit; }   // solo lo ejecuta el cron del hosting; no es accesible por web

$db = new PDO('sqlite:' . $cfg['db']);
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
// Conservación: borra de la cola las solicitudes de más de N meses (ya están en el CRM) y las visitas de más de 13 meses
$db->prepare('DELETE FROM enquiries WHERE received_at < ?')->execute([gmdate('c', strtotime('-' . (int)($cfg['retentionMonths'] ?? 24) . ' months'))]);
foreach (['blocked' => 'at', 'tok' => 'at'] as $tb => $col) { try { $db->prepare("DELETE FROM $tb WHERE $col < ?")->execute([gmdate('c', strtotime($tb === 'blocked' ? '-60 days' : '-2 days'))]); } catch (Throwable $t) {} }  // cuarentena antispam y tokens usados
try { $db->prepare('DELETE FROM hits WHERE day < ?')->execute([gmdate('Y-m-d', strtotime('-13 months'))]); } catch (Throwable $t) {}
$h = 'From: SNAP Web <' . $cfg['from'] . ">\r\nContent-Type: text/plain; charset=utf-8";

foreach ($db->query('SELECT id, type, data FROM enquiries WHERE mail_sent = 0 ORDER BY received_at LIMIT 50') as $r) {   // máx. 50 por pasada: una avalancha no inunda el buzón
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
