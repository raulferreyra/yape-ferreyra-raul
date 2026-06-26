# Evaluación Parcial — Parte A: Diseño y Arquitectura

## Ferreyra Villarriel, Raúl Ricardo | Código: 2221890070

---

## P1.1 — Tabla de Arquitectura Big Data de Yape (2 pts)

Herramienta de IA utilizada para explorar opciones: Claude Sonnet 4.6

| Componente del sistema | Tecnología elegida | Tipo BD / Herramienta | Por qué esta tecnología para Yape |
| --- | --- | --- | --- |
| **Core de pagos** (3.2 M transacciones/día, no puede perder dinero) | **CockroachDB** | NewSQL / Relacional distribuida | Garantiza ACID completo en múltiples nodos vía Raft consensus. Escala horizontalmente agregando nodos sin tiempo de inactividad — crítico cuando un débito sin crédito equivale a pérdida monetaria real e irreversible. |
| **Sesiones de login activo** (15 M usuarios, expira en 30 min) | **Redis Cluster** | Cache en memoria / Key-Value | TTL nativo para expiración automática de sesiones. 15 M sesiones × ~200 bytes ≈ 3 GB en RAM: lecturas en microsegundos vs. milisegundos en disco. Cluster mode distribuye carga entre shards. |
| **Perfil del comerciante** (bodega, restaurante, taxi — atributos distintos) | **MongoDB Atlas** | NoSQL Documental | Schema flexible sin columnas NULL masivas: cada tipo de comercio (bodega, taxi, farmacia) almacena solo sus campos propios. Arrays anidados nativos para carta de restaurante, zonas de cobertura de taxi, código DIGEMID de farmacia. |
| **Historial de transacciones para análisis** (18 TB/año) | **Delta Lake en Databricks (Parquet en S3)** | Data Lakehouse / OLAP | Parquet columnar reduce 60-70 % el tamaño vs. JSON y acelera queries sobre columnas específicas (monto, fecha, tipo). Delta Lake agrega ACID y versionado (time travel) para auditorías regulatorias SBS/SUNAT. |
| **Red de detección de fraude** (ciclo A→B→C→A en < 5 min) | **Neo4j AuraDB** | NoSQL Grafo | Detectar ciclos transaccionales de 3 saltos en SQL requiere 3 JOINs sobre 18 TB — tarda minutos. Cypher (`MATCH (a)-[:PAGO]->(b)-[:PAGO]->(c)-[:PAGO]->(a)`) con índices de grafo nativos resuelve este patrón en milisegundos. |
| **Dashboard ejecutivo** (top 10 distritos, actualización diaria) | **Apache Superset + tablas Gold (Parquet)** | BI / Visualización | Consume directamente las tablas Gold ya agregadas por Databricks (sin tocar el core transaccional). Open-source, integración nativa con Databricks SQL, y actualización diaria con Airflow alineada al ciclo de negocio. |

---

## P1.2 — Teorema CAP (1 pt)

| Componente | Combinación CAP | Propiedad sacrificada | ¿Por qué ese sacrificio es correcto o incorrecto? |
| --- | --- | --- | --- |
| **Core de pagos** (débito/crédito de saldos) | **CP** (Consistency + Partition Tolerance) | **Disponibilidad** | Sacrificio **correcto**: ante una partición de red, el sistema prefiere rechazar la transacción (el usuario ve un error temporal y reintenta) antes que ejecutar un débito sin su crédito correspondiente. Una inconsistencia monetaria es irreversible y genera disputas legales; un error temporal de 2-3 segundos es tolerable. |
| **Historial "mis últimas 50 transacciones"** | **AP** (Availability + Partition Tolerance) | **Consistencia** | Sacrificio **correcto**: el usuario puede ver el historial con un desfase de 1-3 segundos (una transacción reciente aún en propagación). El impacto es cosmético — verá el registro completo en instantes. Priorizar CP aquí dejaría el historial inaccesible durante cualquier partición, degradando la UX sin beneficio real de negocio. |

---

## P1.3 — NewSQL (1 pt)

**a) ¿Qué limitación de Oracle resuelve CockroachDB al escalar de 15M a 50M usuarios?**

Oracle escala **verticalmente** (más CPU/RAM al servidor único), con un límite físico y costo exponencial. Al triplicar los usuarios, el volumen de TPS en hora pico pasaría de ~450 a ~1,350 TPS — Oracle requeriría hardware más poderoso o sharding manual complejo. **CockroachDB escala horizontalmente**: distribuye los datos automáticamente en shards entre nodos commodity, añadiendo servidores sin tiempo de inactividad ni rediseño de esquema. La latencia 45 s que tiene actualmente el sistema Oracle viene precisamente de no poder distribuir la carga de consultas analíticas en el mismo servidor transaccional.

**b) ¿Por qué MongoDB NO puede reemplazar a Oracle para el procesamiento de pagos?**

MongoDB está diseñado para **consistencia eventual** y no garantiza el modelo ACID estricto que requiere el core de pagos. Específicamente: (1) no tiene claves foráneas nativas, por lo que la integridad referencial entre cuentas origen/destino debe mantenerse en la aplicación — superficie de bug crítica; (2) las transacciones multi-documento ACID (desde v4.0) tienen limitaciones de rendimiento a escala y no son el caso de uso primario del motor; (3) no soporta SQL estándar, dificultando los reportes regulatorios que la SBS y SUNAT exigen en formato tabular con JOINs complejos.

**c) ¿Qué mecanismo técnico usa CockroachDB para mantener ACID en múltiples nodos distribuidos?**

**Raft consensus protocol**: cada rango de datos (64 MB por defecto) se replica a múltiples nodos formando un grupo Raft. Una escritura solo se confirma como exitosa cuando la **mayoría de réplicas (quórum)** la han registrado en su log. Esto garantiza consistencia sin un coordinador centralizado único — si un nodo falla, el quórum continúa operando y la transacción no se pierde.

---

Ferreyra Villarriel, Raúl Ricardo | DD283 Big Data | Universidad Autónoma del Perú | 2026-1
