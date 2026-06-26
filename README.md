# Evaluación Parcial — Big Data DD283

## Ferreyra Villarriel, Raúl Ricardo | Código: 2221890070

## Universidad Autónoma del Perú | Semestre 2026-1

---

## Video de sustentación

**Enlace:** `https://______________________________`

> Pendiente de grabación. El video cubrirá los 6 segmentos requeridos:
> presentación, arquitectura Yape (P1.1), pipeline Medallion en Databricks,
> MongoDB Atlas (colecciones + pipeline), Docker Desktop (contenedor corriendo)
> y uso de IA.

---

## Estructura de entrega

```sh
parcial_ferreyra_raul/
├── EVALUACION_PARCIAL_BIGDATA_v1.md   ← Enunciado original del profesor
├── P1_arquitectura.md                  ← Tabla P1.1 + respuestas P1.2 y P1.3
├── P2_databricks_yape.ipynb            ← Notebook con las 4 celdas completadas
├── P3_mongodb_atlas.py                 ← Pasos 1-4 de MongoDB Atlas (inserción + queries + pipeline)
├── P4_docker.py                        ← Conexión Python a contenedor Docker + análisis P4.3
├── screenshots/                        ← Capturas de pantalla (ver detalle abajo)
│   ├── databricks_celda1.png
│   ├── databricks_celda2.png
│   ├── databricks_celda3.png
│   ├── databricks_dashboard.png
│   ├── atlas_collections.png
│   ├── atlas_pipeline_output.png
│   └── docker_desktop.png
└── README.md                           ← Este archivo
```

---

## Resumen de lo implementado

### Parte A — Arquitectura (P1)

- **P1.1**: Tabla completa con 6 componentes de Yape: CockroachDB (core de pagos), Redis Cluster (sesiones), MongoDB Atlas (perfiles de comerciantes), Delta Lake/Databricks (historial analítico 18 TB/año), Neo4j AuraDB (detección de fraude en grafos), Apache Superset (dashboard ejecutivo).
- **P1.2**: CAP Theorem — Core de pagos = CP (sacrifica disponibilidad para garantizar consistencia monetaria); Historial = AP (acepta consistencia eventual sin impacto de negocio).
- **P1.3**: NewSQL — CockroachDB resuelve escalado horizontal de Oracle; MongoDB no es apto por falta de ACID relacional; mecanismo técnico = Raft consensus protocol.

### Parte B — Databricks (P2)

- Pipeline Medallion completo: Bronze (2,000 transacciones sintéticas) → Silver (solo completadas, monto > 0, categorías micro/medio/alto, hora pico, comisión 1.5%) → Gold (top 5 distritos + ingresos por hora).
- Dashboard con 2 gráficos matplotlib exportado a `/FileStore/yape/gold/dashboard_yape.png`.

### Parte C — MongoDB Atlas (P3)

- 5 comerciantes con estructura flexible (bodega, restaurante, farmacia, taxi, empresa).
- 3 queries con operadores `$gt`, `$in`, filtros multi-campo.
- Aggregation pipeline: `$match` → `$group` → `$sort` → `$project` para reporte de facturación por tipo.

### Parte D — Docker (P4)

- Contenedor `yape-mongo-local` con `mongo:7.0` en puerto 27017.
- Conexión Python con autenticación y documento de prueba insertado.
- Análisis P4.3: casos de uso Docker vs Atlas, ventajas M0, comportamiento de datos al `docker rm`.

### Uso de IA

- **Claude Sonnet 4.6** fue utilizado para generar la estructura base de los archivos y explorar opciones tecnológicas en P1.1. Todas las justificaciones fueron adaptadas al caso específico de Yape (fintech peruana, regulación SBS/SUNAT, contexto de 15M usuarios). Los blancos `___` en P2 y P3 fueron completados con comprensión del flujo de datos del pipeline.

---

*DD283 Big Data | Universidad Autónoma del Perú | Evaluación Parcial | Semana 4 | 2026-1*
*Mg. Rubén Quispe Llacctarimay*
