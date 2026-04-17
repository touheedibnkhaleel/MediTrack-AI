from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

app = FastAPI()

DB = "Medi.db"

def conn_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ---------------- MODELS ----------------
class Patient(BaseModel):
    patient_name: str
    is_returning: int

class Appointment(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: str
    appointment_day: str
    appointment_month: int
    appointment_hour: int
    status: str
    fee: int

# ---------------- CREATE ----------------
@app.post("/patient")
def add_patient(p: Patient):
    conn = conn_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO patient_master (patient_name, is_returning) VALUES (?, ?)",
        (p.patient_name, p.is_returning)
    )

    conn.commit()
    conn.close()
    return {"message": "Patient added"}

# ---------------- READ ----------------
@app.get("/patients")
def get_patients():
    conn = conn_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM patient_master")
    data = cur.fetchall()

    conn.close()
    return [dict(row) for row in data]

# ---------------- UPDATE ----------------
@app.put("/appointment/{id}")
def update_status(id: int, status: str):
    conn = conn_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE appointment_transactions SET status=? WHERE appointment_id=?",
        (status, id)
    )

    conn.commit()
    conn.close()

    return {"message": "Updated"}

# ---------------- DELETE ----------------
@app.delete("/appointment/{id}")
def delete_appointment(id: int):
    conn = conn_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM appointment_transactions WHERE appointment_id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return {"message": "Deleted"}