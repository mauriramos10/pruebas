
# Google Sheets (ejemplo de integración)

- Instalar: `pip install gspread oauth2client`
- Crear proyecto en Google Cloud, habilitar Google Sheets API, crear credenciales de servicio y descargar JSON.
- Compartir la hoja con el email del servicio.
- Código de ejemplo (no incluido en app principal):

```python
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)

sh = client.open("Telec-Equipos")
equipos_ws = sh.worksheet("Equipos")
mants_ws = sh.worksheet("Mantenimientos")

# Push de equipos
equipos_ws.clear()
equipos_ws.append_row(["id","name","sap_number","tag","location","criticality","status","description"])
for e in session.query(Equipment).all():
    equipos_ws.append_row([e.id,e.name,e.sap_number,e.tag,e.location,e.criticality,e.status,e.description or ""])

# Pull de equipos (lectura en tiempo real)
rows = equipos_ws.get_all_records()
```

Sugerencia: programar sincronización cada X minutos o al guardar nuevos registros.
