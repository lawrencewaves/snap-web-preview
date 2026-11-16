<?php
// SNAP SURF TRIPS · recibe una solicitud de la web: valida → cola SQLite → email «[WEB-ENQ]» a SNAP.
// Solo responde ok si la solicitud ha quedado guardada en la cola o enviada por email (nunca se pierde en silencio).
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function out(int $code, array $j): void { http_response_code($code); echo json_encode($j); exit; }

$cfgFile = __DIR__ . '/config.php';
if (!is_file($cfgFile)) out(500, ['ok' => false, 'error' => 'config']);
$cfg = require $cfgFile;

if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(405, ['ok' => false, 'error' => 'method']);
// Solo se aceptan envíos desde la propia web (evita que otras webs o robots usen el formulario)
$origin = (string)($_SERVER['HTTP_ORIGIN'] ?? '');
$allowed = array_filter((array)($cfg['allowedOrigins'] ?? []));
if ($allowed && !in_array(rtrim($origin, '/'), $allowed, true)) out(403, ['ok' => false, 'error' => 'origin']);
if (stripos((string)($_SERVER['CONTENT_TYPE'] ?? ''), 'application/json') !== 0) out(415, ['ok' => false, 'error' => 'type']);
$raw = file_get_contents('php://input', false, null, 0, 20000);
$d = json_decode($raw ?: '', true);
if (!is_array($d)) out(400, ['ok' => false, 'error' => 'json']);

// Anti-spam: campo trampa y tiempo mínimo. A los bots se les contesta ok sin guardar nada.
if (!empty($d['website']) || (int)($d['elapsed'] ?? 0) < 3) out(200, ['ok' => true, 'id' => 'WEB-0']);

$clean = function ($v, int $max = 300): string {
    $v = is_scalar($v) ? (string)$v : '';
    // sin caracteres de control ni saltos de línea en campos de una línea (evita inyecciones en cabeceras y registros)
    return mb_substr(trim(preg_replace('/[\x00-\x1F\x7F]/u', ' ', $v) ?? ''), 0, $max);
};
$type = $clean($d['type'] ?? '', 20);
if (!in_array($type, ['individual', 'group', 'partner', 'general'], true)) out(400, ['ok' => false, 'error' => 'type']);
$email = mb_strtolower($clean($d['email'] ?? '', 200));
$name = $clean($d['name'] ?? '', 120);
if (!filter_var($email, FILTER_VALIDATE_EMAIL) || $name === '' || empty($d['consent'])) out(422, ['ok' => false, 'error' => 'required']);

$fields = ['organisation', 'phone', 'country', 'people', 'dates', 'nights', 'level', 'groupType', 'ages', 'destination',
           'budget', 'needs', 'campWebsite', 'listingId', 'packageId', 'page', 'lang'];
$e = ['type' => $type, 'name' => $name, 'email' => $email];
foreach ($fields as $k) { $v = $clean($d[$k] ?? ''); if ($v !== '') $e[$k] = $v; }
$msg = mb_substr(trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', is_scalar($d['message'] ?? '') ? (string)($d['message'] ?? '') : '') ?? ''), 0, 3000); if ($msg !== '') $e['message'] = $msg;
$e['flexible'] = !empty($d['flexible']);
$e['consent'] = ['privacy' => true, 'marketing' => !empty($d['marketing']), 'at' => gmdate('c')];
if (isset($d['matcher']) && is_array($d['matcher'])) {   // respuestas del buscador de surf trip (para el scoring del CRM)
    foreach (array_slice($d['matcher'], 0, 12, true) as $k => $v) {
        if (preg_match('/^[a-z]{1,12}$/', (string)$k)) $e['matcher'][$k] = is_array($v) ? array_map(fn($y) => $clean($y, 40), array_slice($v, 0, 4)) : $clean($v, 60);
    }
}
if (isset($d['utm']) && is_array($d['utm'])) {
    foreach (array_slice($d['utm'], 0, 6, true) as $k => $v) {
        if (preg_match('/^utm_[a-z]{2,10}$/', (string)$k)) $e['utm'][$k] = $clean($v, 120);
    }
}
$id = 'WEB-' . gmdate('Ymd') . '-' . strtoupper(bin2hex(random_bytes(3)));
$e['enquiryId'] = $id;
$e['receivedAt'] = gmdate('c');
$ipHash = hash('sha256', ($cfg['salt'] ?? '') . ($_SERVER['REMOTE_ADDR'] ?? ''));

// 1) Cola
$saved = false;
try {
    $db = new PDO('sqlite:' . $cfg['db']);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $db->exec('CREATE TABLE IF NOT EXISTS enquiries (id TEXT PRIMARY KEY, received_at TEXT, type TEXT, email TEXT, ip TEXT, data TEXT, mail_sent INTEGER DEFAULT 0)');
    $q = $db->prepare("SELECT COUNT(*) FROM enquiries WHERE ip = ? AND received_at > ?");
    $q->execute([$ipHash, gmdate('c', time() - 3600)]);
    if ((int)$q->fetchColumn() >= (int)($cfg['maxPerHour'] ?? 5)) out(429, ['ok' => false, 'error' => 'rate']);
    $db->prepare('INSERT INTO enquiries (id, received_at, type, email, ip, data) VALUES (?,?,?,?,?,?)')
       ->execute([$id, $e['receivedAt'], $type, $email, $ipHash, json_encode($e, JSON_UNESCAPED_UNICODE)]);
    $saved = true;
} catch (Throwable $t) { error_log('SNAP enquiry db: ' . $t->getMessage()); }

// 2) Email estructurado para el registro en el CRM
$subject = "[WEB-ENQ] $id · $type" . (isset($e['listingId']) ? ' · ' . $e['listingId'] : '');
$body = json_encode($e, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$headers = 'From: SNAP Web <' . $cfg['from'] . ">\r\nContent-Type: text/plain; charset=utf-8\r\nX-SNAP-Enquiry: $id";
$sent = @mail($cfg['to'], '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);
if ($sent && $saved) { try { $db->prepare('UPDATE enquiries SET mail_sent = 1 WHERE id = ?')->execute([$id]); } catch (Throwable $t) {} }

if (!$saved && !$sent) out(500, ['ok' => false, 'error' => 'store']);
out(200, ['ok' => true, 'id' => $id]);
