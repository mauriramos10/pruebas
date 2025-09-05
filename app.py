
import os
from io import BytesIO
from datetime import datetime
from flask import Flask, jsonify, request, send_file, send_from_directory, render_template
from flask_cors import CORS
from werkzeug.exceptions import NotFound, BadRequest
from dotenv import load_dotenv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
import qrcode

from models import Base, Equipment, Maintenance, get_engine_and_session

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
app.config["SECRET_KEY"] = SECRET_KEY

engine, SessionLocal = get_engine_and_session(os.getenv("DATABASE_URL", "sqlite:///telec.db"))
Base.metadata.bind = engine

def db_session():
    return scoped_session(SessionLocal)

@app.cli.command("db-init")
def db_init():
    Base.metadata.create_all(engine)
    print("DB initialized")

# --------------- Views (basic) -----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/scanner")
def scanner():
    return render_template("scanner.html")

@app.route("/equipment/<int:equipment_id>")
def equipment_page(equipment_id):
    return render_template("equipment.html", equipment_id=equipment_id)

# --------------- API: Equipment ----------------
@app.get("/api/equipment")
def list_equipment():
    s = db_session()
    try:
        q = s.query(Equipment)
        search = request.args.get("q")
        if search:
            like = f"%{search}%"
            q = q.filter((Equipment.name.ilike(like)) | (Equipment.sap_number.ilike(like)) | (Equipment.tag.ilike(like)))
        items = [e.to_dict() for e in q.order_by(Equipment.id.desc()).all()]
        return jsonify(items)
    finally:
        s.remove()

@app.post("/api/equipment")
def create_equipment():
    data = request.json or {}
    required = ["name"]
    if not all(k in data and data[k] for k in required):
        raise BadRequest("Falta 'name'")
    s = db_session()
    try:
        e = Equipment(
            name=data["name"],
            sap_number=data.get("sap_number"),
            tag=data.get("tag"),
            location=data.get("location"),
            criticality=data.get("criticality","Media"),
            status=data.get("status","Operativo"),
            description=data.get("description"),
        )
        s.add(e)
        s.commit()
        return jsonify(e.to_dict()), 201
    finally:
        s.remove()

@app.get("/api/equipment/<int:equipment_id>")
def get_equipment(equipment_id):
    s = db_session()
    try:
        e = s.get(Equipment, equipment_id)
        if not e:
            raise NotFound("Equipo no encontrado")
        return jsonify(e.to_dict(detail=True))
    finally:
        s.remove()

@app.put("/api/equipment/<int:equipment_id>")
def update_equipment(equipment_id):
    s = db_session()
    try:
        e = s.get(Equipment, equipment_id)
        if not e:
            raise NotFound("Equipo no encontrado")
        data = request.json or {}
        for field in ["name","sap_number","tag","location","criticality","status","description"]:
            if field in data:
                setattr(e, field, data[field])
        s.commit()
        return jsonify(e.to_dict(detail=True))
    finally:
        s.remove()

@app.delete("/api/equipment/<int:equipment_id>")
def delete_equipment(equipment_id):
    s = db_session()
    try:
        e = s.get(Equipment, equipment_id)
        if not e:
            raise NotFound("Equipo no encontrado")
        s.delete(e)
        s.commit()
        return "", 204
    finally:
        s.remove()

# --------------- API: Maintenance --------------
@app.get("/api/maintenance")
def list_maintenance():
    s = db_session()
    try:
        eq_id = request.args.get("equipment_id", type=int)
        q = s.query(Maintenance)
        if eq_id:
            q = q.filter(Maintenance.equipment_id == eq_id)
        items = [m.to_dict() for m in q.order_by(Maintenance.date.desc()).all()]
        return jsonify(items)
    finally:
        s.remove()

@app.post("/api/maintenance")
def create_maintenance():
    data = request.json or {}
    required = ["equipment_id","performed"]
    if not all(k in data for k in required):
        raise BadRequest("Faltan campos: equipment_id, performed")
    s = db_session()
    try:
        m = Maintenance(
            equipment_id=data["equipment_id"],
            date=datetime.fromisoformat(data.get("date")) if data.get("date") else datetime.utcnow(),
            performed=bool(data["performed"]),
            notes=data.get("notes"),
            technician=data.get("technician"),
            hours=data.get("hours", 0.0),
        )
        s.add(m)
        s.commit()
        return jsonify(m.to_dict()), 201
    finally:
        s.remove()

# --------------- Export to Excel ---------------
@app.get("/export/excel")
def export_excel():
    s = db_session()
    try:
        eq = pd.DataFrame([e.to_dict() for e in s.query(Equipment).all()])
        mt = pd.DataFrame([m.to_dict() for m in s.query(Maintenance).all()])
        os.makedirs("exports", exist_ok=True)
        path = os.path.join("exports", "export_equipment.xlsx")
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            (eq if not eq.empty else pd.DataFrame(columns=["id","name","sap_number","tag","location","criticality","status","description"])).to_excel(writer, sheet_name="Equipos", index=False)
            (mt if not mt.empty else pd.DataFrame(columns=["id","equipment_id","date","performed","notes","technician","hours"])).to_excel(writer, sheet_name="Mantenimientos", index=False)
        return send_file(path, as_attachment=True, download_name="export_equipment.xlsx")
    finally:
        s.remove()

# --------------- QR generation -----------------
@app.get("/qr/<int:equipment_id>")
def qr_equipment(equipment_id):
    base = os.getenv("BASE_URL", "http://127.0.0.1:5000")
    url = f"{base}/equipment/{equipment_id}"
    img = qrcode.make(url)
    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return send_file(bio, mimetype="image/png", download_name=f"equipment_{equipment_id}.png")

# --------------- Static helper -----------------
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)
