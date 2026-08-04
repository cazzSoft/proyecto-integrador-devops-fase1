# Evidencia del diagnóstico DevOps

## Flujo de valor actual

| Etapa | Responsable | Actividad actual | Evidencia | Trabajo/espera | Riesgo observado |
|---|---|---|---|---|---|
| Modificación | Desarrollador | Editar frontend o backend localmente | Archivos modificados | No medido | Cambios sin trazabilidad si no se confirman |
| Integración | Desarrollador | Unir cambios manualmente | Commit local | No medido | Conflictos y validación tardía |
| Construcción | Desarrollador | Ejecutar `docker compose up --build` | Salida de consola | Varios minutos | Depende del equipo y de la red |
| Base de datos | Contenedor backend | Ejecutar `prisma db push` al iniciar | Log del backend | En cada arranque | Cambio de esquema sin migración versionada |
| Pruebas | Desarrollador | Recorrer el CRUD en el navegador | Observación manual | Variable | No existe evidencia repetible |
| Aprobación | Desarrollador | Decidir si la versión funciona | Criterio personal | Variable | Ausencia de revisión independiente |
| Despliegue | Desarrollador | Ejecutar comandos en el destino | Consola | No medido | Sin pipeline, rollback ni segregación de ambientes |
| Operación | Desarrollador | Revisar logs ante un fallo | Log Fastify | Reactivo | Sin métricas, alertas ni política de retención |

## Priorización

Se utiliza una escala de impacto y probabilidad de 1 (bajo) a 3 (alto). La prioridad es el producto de ambas variables.

| Hallazgo | Categoría | Impacto | Probabilidad | Prioridad | Fundamento |
|---|---|---:|---:|---:|---|
| Sin pipeline CI/CD | Proceso/herramienta | 3 | 3 | 9 | Toda validación depende del desarrollador y puede omitirse |
| Sin pruebas automatizadas | Proceso | 3 | 3 | 9 | Cada modificación puede introducir regresiones no detectadas |
| Dependencias vulnerables | Seguridad | 3 | 3 | 9 | `npm audit` reportó 2 hallazgos en frontend y 6 altos en backend |
| Credenciales en la práctica original | Seguridad | 3 | 2 | 6 | Los secretos podían quedar expuestos en el repositorio público |
| Sin observabilidad | Herramienta | 2 | 3 | 6 | Los fallos se conocen por logs o por el usuario, no por alertas |
| Sin rollback ni respaldo | Continuidad | 3 | 2 | 6 | Un cambio defectuoso puede prolongar la indisponibilidad |

## Diagnóstico CALMS

| Dimensión | Fortaleza inicial | Brecha | Acción propuesta |
|---|---|---|---|
| Cultura | Proyecto pequeño con responsabilidad identificable | Conocimiento concentrado en una persona | Documentar decisiones y revisar resultados sin culpa |
| Automatización | Docker Compose reproduce tres servicios | No hay CI, pruebas ni entrega automatizada | Automatizar build, pruebas y controles de seguridad |
| Lean | Arquitectura simple y cambios potencialmente pequeños | Retrabajo por pruebas tardías | Lotes pequeños y validación temprana por commit |
| Medición | Fastify genera logs | No hay línea base DORA ni métricas técnicas | Instrumentar pipeline, incidentes y cobertura |
| Sharing | Git permite compartir código | La práctica llegó como ZIP y sin README | Repositorio público, README, diagramas y runbook |

## Riesgos y tratamientos

| Riesgo | Tratamiento inicial | Indicador |
|---|---|---|
| Exposición de secretos | `.gitignore`, `.env.example` y secretos del repositorio | 0 secretos detectados por commit |
| Vulnerabilidades de dependencias | Auditoría automática y actualización controlada | Hallazgos por severidad y versión |
| Cambios defectuosos | Build y pruebas obligatorias antes de integrar | Tasa de fallos del cambio |
| Pérdida de datos | Respaldo, restauración probada y migraciones Prisma | Éxito de restauración y RPO/RTO |
| Indisponibilidad prolongada | Healthchecks, rollback y runbook | Tiempo de recuperación |
| Registros con datos personales | Minimización, acceso restringido y retención | Incidentes de privacidad y cumplimiento de retención |

## Trazabilidad problema-práctica-métrica

| Problema | Práctica DevOps | Herramienta candidata | Métrica | Resultado esperado |
|---|---|---|---|---|
| Validación manual | Integración continua | GitHub Actions o Jenkins | Lead time y frecuencia | Evidencia automática y entregas más frecuentes |
| Pruebas inexistentes | Pruebas tempranas | Vitest y una herramienta de API | Cobertura y tasa de fallos | Menos regresiones y retrabajo |
| Dependencias vulnerables | DevSecOps / shift-left | `npm audit`, Dependabot y SAST | Hallazgos por severidad | Riesgo visible antes del despliegue |
| Secretos en archivos | Gestión de configuración | GitHub Secrets y escaneo de secretos | Secretos detectados | Cero credenciales versionadas |
| Fallos detectados tarde | Observabilidad | Logs estructurados y OpenTelemetry | Tiempo de detección/recuperación | Respuesta más rápida |

