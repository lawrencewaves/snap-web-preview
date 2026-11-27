<?php
// SNAP SURF TRIPS · recibe una solicitud de la web: valida → cola SQLite → email «[WEB-ENQ]» a SNAP.
// Solo responde ok si la solicitud ha quedado guardada en la cola o enviada por email (nunca se pierde en silencio).
declare(strict_types=1);
ini_set('display_errors', '0');   // nunca mostrar errores al visitante (rutas, versiones); van al log del servidor
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
if ($allowed) { if (!in_array(rtrim($origin, '/'), $allowed, true)) out(403, ['ok' => false, 'error' => 'origin']); }
elseif (strcasecmp((string)parse_url($origin, PHP_URL_HOST), (string)preg_replace('/:\d+$/', '', (string)($_SERVER['HTTP_HOST'] ?? ''))) !== 0) out(403, ['ok' => false, 'error' => 'origin']);   // sin lista configurada: el Origin debe ser este mismo sitio (los navegadores siempre lo envían en un POST)
if (stripos((string)($_SERVER['CONTENT_TYPE'] ?? ''), 'application/json') !== 0) out(415, ['ok' => false, 'error' => 'type']);
$raw = file_get_contents('php://input', false, null, 0, 20000);
$d = json_decode($raw ?: '', true);
if (!is_array($d)) out(400, ['ok' => false, 'error' => 'json']);

// ── Anti-spam por capas (sin servicios externos). A los bots se les contesta ok para que no se adapten, pero no llega nada al CRM:
// lo bloqueado queda en cuarentena (tabla `blocked`, 60 días) y se revisa en api/stats.php?key=…
$ipHash = hash('sha256', ($cfg['salt'] ?? '') . ($_SERVER['REMOTE_ADDR'] ?? ''));
function quarantine(array $cfg, string $why, array $d, string $ipHash): void {
    try {
        $b = new PDO('sqlite:' . $cfg['db']);
        $b->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $b->exec('CREATE TABLE IF NOT EXISTS blocked (at TEXT, reason TEXT, ip TEXT, email TEXT, data TEXT)');
        $c = $b->prepare('SELECT COUNT(*) FROM blocked WHERE ip = ? AND at > ?'); $c->execute([$ipHash, gmdate('c', time() - 3600)]);
        if ((int)$c->fetchColumn() >= 10) out(429, ['ok' => false, 'error' => 'rate']);   // un robot insistente deja de guardarse y se le corta
        $b->prepare('INSERT INTO blocked VALUES (?,?,?,?,?)')->execute([gmdate('c'), $why, $ipHash,
            mb_substr((string)($d['email'] ?? ''), 0, 200), mb_substr((string)json_encode($d, JSON_UNESCAPED_UNICODE), 0, 4000)]);
    } catch (Throwable $t) { error_log('SNAP quarantine: ' . $t->getMessage()); }
    out(200, ['ok' => true, 'id' => 'WEB-0']);
}
// 1) Campo trampa (invisible para personas)
if (!empty($d['fax_number']) || !empty($d['website'])) quarantine($cfg, 'honeypot', $d, $ipHash);
// 2) Token firmado de api/token.php: firma válida, entre 4 s y 2 h de antigüedad (medida aquí, no en el navegador) y de un solo uso.
//    Sin token válido o caducado → 409: el formulario pide otro y reintenta solo, así una persona nunca pierde su mensaje.
$tp = explode('.', (string)($d['tok'] ?? ''));
if (count($tp) !== 3 || !ctype_digit($tp[0]) || !preg_match('/^[a-f0-9]{16}$/', $tp[1]) || !preg_match('/^[a-f0-9]{32}$/', $tp[2])
    || !hash_equals(substr(hash_hmac('sha256', $tp[0] . '.' . $tp[1], hash('sha256', (string)($cfg['salt'] ?? '') . 'tok')), 0, 32), $tp[2])
    || time() - (int)$tp[0] > 7200) out(409, ['ok' => false, 'error' => 'token']);
if (time() - (int)$tp[0] < 4) quarantine($cfg, 'fast', $d, $ipHash);
// 3) Filtro de contenido: spam típico de «mejoramos tu SEO / diseño web / casino…». Puntúa; a partir de 4 se bloquea.
function spam_score(string $t): array {
    $t = mb_strtolower($t); $s = 0; $why = [];
    $add = function (string $n, int $p) use (&$s, &$why) { $s += $p; $why[] = $n; };
    if (preg_match('/\b(seo|search engine optimi[sz]ation|posicionamiento (web|seo)|primera p[aá]gina de google)\b/u', $t)
        && preg_match('/\b(rank\w*|google|bing|traffic|competitors?|backlinks?|website|web|tr[aá]fico|competencia|posicion\w*)\b/u', $t)) $add('seo', 4);
    foreach ([
        'your website' => '/\b(your|tu|su) (web ?site|p[aá]gina web|sitio web)\b.*\b(our (team|agency|services)|we (can|will|offer|would)|podemos|ofrecemos|nuestro (equipo|servicio))/su',
        'reply-number' => '/\b(reply|respond\w*|responde\w*)\b.{0,40}\b(contact )?(number|phone|n[uú]mero|tel[eé]fono)\b/su',
        'free-offer' => '/\bfree (audit|quote|consultation|trial|report)\b|\b(auditor[ií]a|presupuesto|consulta) gratuit[ao]\b/u',
        'webdesign' => '/\b(web ?(site)? ?(design|redesign|development)|dise[ñn]o web|desarrollo web|marketing digital|lead generation)\b/u',
        'linkbuilding' => '/\b(guest post|backlinks?|link ?building)\b/u',
        'scam' => '/\b(crypto\w*|bitcoin|casino|forex|viagra|investment opportunity|loan offer|inversi[oó]n garantizada)\b/u',
        'shortener' => '/\b(bit\.ly|tinyurl|t\.co|goo\.gl)\//u',
    ] as $n => $re) if (preg_match($re, $t)) $add($n, 2);
    $links = preg_match_all('#https?://|www\.#u', $t);
    if ($links >= 4) $add('links4', 4); elseif ($links >= 2) $add('links2', 2);
    return [$s, $why];
}
[$sc, $why] = spam_score(implode("\n", array_map(fn($k) => is_scalar($d[$k] ?? '') ? (string)($d[$k] ?? '') : '', ['message', 'name', 'organisation', 'needs'])));
if ($sc >= 4) quarantine($cfg, 'content:' . implode(',', $why), $d, $ipHash);

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

// Clave de idempotencia (la genera el navegador por envío): un reintento con la misma clave no crea otra solicitud
$idem = preg_match('/^[A-Za-z0-9._-]{8,64}$/', (string)($d['idemKey'] ?? '')) ? (string)$d['idemKey'] : '';
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

// 1) Cola
$saved = false;
try {
    $db = new PDO('sqlite:' . $cfg['db']);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $db->exec('CREATE TABLE IF NOT EXISTS enquiries (id TEXT PRIMARY KEY, received_at TEXT, type TEXT, email TEXT, ip TEXT, data TEXT, mail_sent INTEGER DEFAULT 0)');
    $db->exec('CREATE TABLE IF NOT EXISTS idem (k TEXT PRIMARY KEY, id TEXT, at TEXT)');
    if ($idem !== '') {
        $db->prepare('DELETE FROM idem WHERE at < ?')->execute([gmdate('c', time() - 172800)]);
        $q = $db->prepare('SELECT id FROM idem WHERE k = ?'); $q->execute([$idem]);
        $prev = $q->fetchColumn();
        if ($prev) out(200, ['ok' => true, 'id' => (string)$prev]);   // ya recibida: misma respuesta, sin guardar ni enviar nada
    }
    // El token solo vale una vez (va después de la clave de idempotencia: un reintento legítimo recibe su respuesta sin gastar otro)
    $db->exec('CREATE TABLE IF NOT EXISTS tok (n TEXT PRIMARY KEY, at TEXT)');
    $db->prepare('DELETE FROM tok WHERE at < ?')->execute([gmdate('c', time() - 14400)]);
    $r = $db->prepare('INSERT OR IGNORE INTO tok (n, at) VALUES (?,?)'); $r->execute([$tp[1], gmdate('c')]);
    if ($r->rowCount() === 0) out(409, ['ok' => false, 'error' => 'token']);
    $q = $db->prepare("SELECT COUNT(*) FROM enquiries WHERE ip = ? AND received_at > ?");
    $q->execute([$ipHash, gmdate('c', time() - 3600)]);
    if ((int)$q->fetchColumn() >= (int)($cfg['maxPerHour'] ?? 5)) out(429, ['ok' => false, 'error' => 'rate']);
    if ($idem !== '') {   // reserva la clave antes de guardar: dos peticiones simultáneas no pueden pasar las dos
        $r = $db->prepare('INSERT OR IGNORE INTO idem (k, id, at) VALUES (?,?,?)'); $r->execute([$idem, $id, $e['receivedAt']]);
        if ($r->rowCount() === 0) { $q = $db->prepare('SELECT id FROM idem WHERE k = ?'); $q->execute([$idem]); out(200, ['ok' => true, 'id' => (string)$q->fetchColumn()]); }
    }
    try {
        $db->prepare('INSERT INTO enquiries (id, received_at, type, email, ip, data) VALUES (?,?,?,?,?,?)')
           ->execute([$id, $e['receivedAt'], $type, $email, $ipHash, json_encode($e, JSON_UNESCAPED_UNICODE)]);
    } catch (Throwable $t) { if ($idem !== '') { $db->prepare('DELETE FROM idem WHERE k = ?')->execute([$idem]); } throw $t; }
    $saved = true;
} catch (Throwable $t) { error_log('SNAP enquiry db: ' . $t->getMessage()); }

// 2) Email estructurado para el registro en el CRM
$subject = "[WEB-ENQ] $id · $type" . (isset($e['listingId']) ? ' · ' . $e['listingId'] : '');
$body = json_encode($e, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
$headers = 'From: SNAP Web <' . $cfg['from'] . ">\r\nContent-Type: text/plain; charset=utf-8\r\nX-SNAP-Enquiry: $id";
$flood = false;
try { $fq = $db->prepare('SELECT COUNT(*) FROM enquiries WHERE received_at > ?'); $fq->execute([gmdate('c', time() - 3600)]); $flood = (int)$fq->fetchColumn() > (int)($cfg['maxMailsPerHour'] ?? 30); } catch (Throwable $t) {}
$sent = $flood && $saved ? false : @mail($cfg['to'], '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers);
if ($sent && $saved) { try { $db->prepare('UPDATE enquiries SET mail_sent = 1 WHERE id = ?')->execute([$id]); } catch (Throwable $t) {} }

if (!$saved && !$sent) out(500, ['ok' => false, 'error' => 'store']);
out(200, ['ok' => true, 'id' => $id]);
