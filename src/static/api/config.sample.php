<?php
// Copiar como config.php y rellenar. No subir config.php a ningún repositorio.
return [
    'to'         => 'BUZON-DE-SNAP',                 // buzón que lee la tarea de bandeja de SNAP (el Gmail de SNAP)
    'from'       => 'web@TU-DOMINIO.com',            // dirección del propio dominio (necesaria para que el email no caiga en spam)
    'db'         => __DIR__ . '/data/enquiries.sqlite',
    'salt'       => 'CAMBIAR-por-un-texto-largo-aleatorio',
    'cronKey'    => 'CAMBIAR-por-otro-texto-largo-aleatorio',
    'maxPerHour' => 5,
    'allowedOrigins' => ['https://www.TU-DOMINIO.com', 'https://TU-DOMINIO.com'],   // vacío = sin comprobar (solo para pruebas)
    'retentionMonths' => 24,                          // solicitudes sin reserva: se borran a los 24 meses (política de privacidad)
];
