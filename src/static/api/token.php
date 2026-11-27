<?php
// SNAP · token firmado para el formulario. El navegador lo pide al empezar a rellenarlo y lo devuelve al enviar;
// enquiry.php comprueba la firma, la antigüedad medida por el servidor y que sea de un solo uso. Sin cookies ni datos personales.
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');
if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'GET') { http_response_code(405); exit; }
$cfg = require __DIR__ . '/config.php';
$t = time() . '.' . bin2hex(random_bytes(8));
echo json_encode(['t' => $t . '.' . substr(hash_hmac('sha256', $t, hash('sha256', (string)($cfg['salt'] ?? '') . 'tok')), 0, 32)]);
