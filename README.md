# 📘 Guía de uso – Pantaleon · Consulta de Equipos

Este proyecto permite consultar **equipos, componentes y documentos técnicos** desde un navegador web.  
Está diseñado para que cualquier mecánico o supervisor pueda acceder fácilmente a la información.

---

## 📂 Estructura de archivos

```
/index.html            → Página principal
/logo.png              → Logo de la empresa
/equipos.csv           → Lista de equipos con SAP, nombre y ubicación técnica
/componentes.csv       → Lista de componentes asociados a cada SAP
/docs/                 → Carpeta con documentos técnicos en PDF
   └── ejemplo.pdf
```

---

## 🔄 Cómo actualizar la base de datos

### 1. Actualizar **equipos**
1. Abrir el archivo en Excel: `BASE DE DATOS EQUIPO, UB TEC, SAP.xlsx`.
2. Guardarlo como **CSV (UTF-8)** con el nombre:
   ```
   equipos.csv
   ```
3. Subirlo al repositorio en GitHub reemplazando el anterior.

**Encabezados obligatorios**:
```
ubicacion tecnica, codigo sap, nombre del equipo
```

---

### 2. Actualizar **componentes**
1. Abrir el archivo en Excel: `componentes.xlsx`.
2. Guardarlo como **CSV (UTF-8)** con el nombre:
   ```
   componentes.csv
   ```
3. Subirlo al repositorio en GitHub reemplazando el anterior.

**Encabezados obligatorios**:
```
codigo sap, componente, caracteristicas, marca, codigo de repuesto, descripcion, posicion, ano
```

---

### 3. Agregar documentos técnicos
1. Guardar el archivo PDF en la carpeta `/docs/`.
2. Editar el archivo `index.html` en el bloque `documentosPorSAP`.

Ejemplo:
```js
const documentosPorSAP = {
  "140001": ["NUEVOEQUIPO.pdf"],             // un documento
  "140002": ["DOC1.pdf", "DOC2.pdf"]         // varios documentos
};
```

Los botones aparecerán automáticamente en pantalla como:
```
📄 Consulta NUEVOEQUIPO
📄 Consulta DOC1
📄 Consulta DOC2
```

---

## 🚀 Cómo publicar cambios
1. Subir todos los archivos actualizados al repositorio en GitHub.
2. Si tienes GitHub Pages activado, los cambios estarán disponibles en línea.
3. Si no ves los cambios, forzar recarga con **Ctrl + Shift + R**.

---

## 📷 Funciones incluidas
- 🔍 Búsqueda en tiempo real por **SAP** o **nombre de equipo**.  
- 📑 Tabla con componentes (características, marca, repuesto, descripción, posición, año).  
- 📂 Documentos técnicos asociados, con botones en fila.  
- 📷 Escáner QR para llenar automáticamente el campo SAP.  
- 🕒 Fecha y hora en el encabezado.  
- 👤 Campo editable para asignar **responsable** (guardado en el navegador).  

---

## ✏️ Notas importantes
- Los nombres de los documentos en `/docs` deben coincidir exactamente con los que aparecen en `documentosPorSAP`.  
- Los CSV deben guardarse siempre con **separador de comas (`,`)** y en codificación **UTF-8**.  
- No borres columnas ni cambies los encabezados, solo agrega o modifica filas.  
