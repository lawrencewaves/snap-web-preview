<?php
// Copiar como config.php y rellenar. No subir config.php a ningún repositorio.
return [
    'to'         => 'BUZON-DE-SNAP',                 // buzón que lee la tarea de bandeja de SNAP (el Gmail de SNAP)
    'from'       => 'web@TU-DOMINIO.com',            // dirección del propio dominio (necesaria para que el email no caiga en spam)
    'db'         => __DIR__ . '/data/enquiries.sqlite',
    'salt'       => 'CAMBIAR-por-un-texto-largo-aleatorio',
    'cronKey'    => 'CAMBIAR-por-otro-texto-largo-aleatorio',
    'maxPerHour' => 5,                                // solicitudes por IP y hora
    'maxMailsPerHour' => 30,                          // tope de avisos por email por hora (si se supera, se guardan y el resumen diario los reenvía)
    'allowedOrigins' => ['https://www.TU-DOMINIO.com', 'https://TU-DOMINIO.com'],   // vacío = sin comprobar (solo para pruebas)
    'retentionMonths' => 24,                          // solicitudes sin reserva: se borran a los 24 meses (política de privacidad)
];
