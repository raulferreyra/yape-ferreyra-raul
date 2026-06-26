# ============================================================
# P4 — Docker Desktop: MongoDB local en contenedor
# Ferreyra Villarriel, Raúl Ricardo | Código: 2221890070
# DD283 Big Data | Universidad Autónoma del Perú | 2026-1
# ============================================================
# ANTES de ejecutar este script, levantar el contenedor:
#
#   docker pull mongo:7.0
#
#   docker run -d \
#     --name yape-mongo-local \
#     -p 27017:27017 \
#     -e MONGO_INITDB_ROOT_USERNAME=admin \
#     -e MONGO_INITDB_ROOT_PASSWORD=yape2026 \
#     mongo:7.0
#
#   docker ps
#
# ============================================================

from pymongo import MongoClient

# ============================================================
# PASO 2 (4.2) — Conectar Python al MongoDB Docker (localhost)
# ============================================================
client_docker = MongoClient(
    "mongodb://admin:yape2026@localhost:27017/",
    authSource="admin"
)

db_local = client_docker["yape_local"]
col_local = db_local["comerciantes_test"]

# Insertar el mismo comerciante del Paso 2 de Atlas
col_local.insert_one({
    "nombre_comercio": "Bodega Test Docker",
    "tipo": "bodega",
    "distrito": "Lima",
    "monto_mensual_soles": 1500.00,
    "yape_activo": True,
    "entorno": "docker_local"   # Campo que indica que es entorno local
})

# Verificar
doc = col_local.find_one({"nombre_comercio": "Bodega Test Docker"})
print("✅ Documento guardado en MongoDB Docker:")
print(f"   Nombre:   {doc['nombre_comercio']}")
print(f"   Entorno:  {doc['entorno']}")
print(f"   ID:       {doc['_id']}")

# Mostrar todos los documentos en la colección
print(f"\nTotal documentos en Docker: {col_local.count_documents({})}")

# ============================================================
# PASO 3 (4.3) — Diferencia entre Docker y Atlas
# ============================================================
print("""
============================================================
P4.3 — ANÁLISIS: Docker vs MongoDB Atlas
============================================================

a) ¿Cuándo usarías MongoDB en Docker en lugar de Atlas para Yape?

   Usaría Docker cuando el equipo de desarrollo necesita un entorno
   local sin acceso a internet o sin costos por operaciones (desarrollo
   offline, pruebas de integración en CI/CD, demos sin conexión). Docker
   garantiza que todos los desarrolladores usan exactamente la misma
   versión de MongoDB (mongo:7.0), eliminando el clásico "en mi máquina
   funciona". También es útil para pruebas destructivas (borrar colecciones,
   probar migraciones) sin arriesgar datos reales en Atlas.

b) ¿Qué ventaja tiene Atlas M0 sobre el contenedor Docker en contexto universitario?

   Atlas M0 es accesible desde cualquier dispositivo con internet sin
   instalar nada — ideal para trabajo en grupo donde cada integrante usa
   su propio laptop (algunos con 4 GB de RAM donde Docker consume recursos
   considerables). Además, Atlas incluye interfaz gráfica (Browse Collections,
   Charts, Aggregation Builder) que facilita visualizar y depurar los datos
   sin herramientas adicionales. No requiere que Docker Desktop esté
   instalado ni configurado — reduce la fricción para empezar.

c) ¿Qué sucede con los datos al hacer docker stop + docker rm?

   Al ejecutar:
     docker stop yape-mongo-local  → detiene el contenedor (datos en
       volumen interno del contenedor, aún existen pero el proceso para)
     docker rm yape-mongo-local    → ELIMINA el contenedor y sus datos
       internos de forma PERMANENTE e irreversible.

   Los datos del contenedor Docker se PIERDEN porque no se montó un
   volumen persistente externo (-v /ruta/local:/data/db). Para preservar
   datos en Docker, se debe usar volumen nombrado:
     docker run -d --name yape-mongo-local -p 27017:27017
       -v yape_data:/data/db -e MONGO_INITDB_ROOT_USERNAME=admin
       -e MONGO_INITDB_ROOT_PASSWORD=yape2026 mongo:7.0

   Los datos de Atlas M0 permanecen intactos — están en servidores de
   AWS São Paulo gestionados por MongoDB Inc. con réplicas automáticas
   en 3 zonas de disponibilidad. Ninguna operación local los afecta.
""")
