
# TELEC Equipment Maintenance App (Starter)

Stack: Flask + SQLAlchemy (SQLite by default), REST API, basic HTML/JS frontend, QR codes, Excel export.
Optional integrations outlined for Google Sheets / Excel Online.

## Quickstart
1) Create a virtual env and install deps:
```
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
2) Initialize DB and run:
```
cp .env.example .env
flask --app app.py db-init
flask --app app.py run
```
Visit: http://127.0.0.1:5000

## Features
- CRUD de equipos y mantenimientos (REST + UI mínima).
- Exportación a Excel: `/export/excel` genera `export_equipment.xlsx` con equipos y mantenimientos.
- Generación de QR por equipo: `/qr/<equipment_id>` devuelve PNG (incrusta URL de consulta).
- Lector de QR en el navegador (HTML5): página "Scanner" para abrir cámara y leer el código (móvil/PC).
- Estructura lista para escalar a PostgreSQL.
- Listados con búsqueda simple en frontend.

## Endpoints clave
- `GET /api/equipment` (listado), `POST /api/equipment` (crear), `GET /api/equipment/<id>` (detalle),
  `PUT /api/equipment/<id>`, `DELETE /api/equipment/<id>`.
- `GET /api/maintenance?equipment_id=<id>` (listar por equipo), `POST /api/maintenance` (crear).
- `GET /export/excel` → genera Excel en `./exports/export_equipment.xlsx` y lo descarga.

## Variables de entorno (.env)
```
FLASK_ENV=development
SECRET_KEY=change-me
DATABASE_URL=sqlite:///telec.db
BASE_URL=http://127.0.0.1:5000
```

Para PostgreSQL: `DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/telec`

## Integración con Google Sheets (opcional)
- Estrategia: sincronizar equipos a pestaña "Equipos" y mantenimientos a "Mantenimientos".
- Usar `gspread` + credenciales de servicio. Ver `integrations/google_sheets_example.md` (plantilla).

## Integración con Excel Online (Microsoft 365) (opcional)
- Usar Microsoft Graph (API de Excel). Ver `integrations/excel_online_notes.md`.

## Licencia
MIT
