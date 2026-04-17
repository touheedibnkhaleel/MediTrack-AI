import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("Medi.db")
cursor = conn.cursor()

# ---------------- DROP ----------------
cursor.executescript("""
DROP TABLE IF EXISTS appointment_transactions;
DROP TABLE IF EXISTS doctor_master;
DROP TABLE IF EXISTS patient_master;
DROP TABLE IF EXISTS clinic_master;
DROP TABLE IF EXISTS city_master;
""")

# ---------------- CREATE ----------------
cursor.executescript("""
CREATE TABLE city_master (
    city_id INTEGER PRIMARY KEY,
    city_name TEXT
);

CREATE TABLE clinic_master (
    clinic_id INTEGER PRIMARY KEY,
    clinic_name TEXT,
    city_id INTEGER
);

CREATE TABLE doctor_master (
    doctor_id INTEGER PRIMARY KEY,
    doctor_name TEXT,
    department TEXT,
    level TEXT,
    clinic_id INTEGER
);

CREATE TABLE patient_master (
    patient_id INTEGER PRIMARY KEY,
    patient_name TEXT,
    is_returning INTEGER
);

CREATE TABLE appointment_transactions (
    appointment_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date TEXT,
    appointment_day TEXT,
    appointment_month INTEGER,
    appointment_hour INTEGER,
    status TEXT,
    fee INTEGER
);
""")

cities = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Multan"]
departments = ["General", "Cardiology", "Ortho", "Dermatology", "Pediatrics"]
levels = ["Junior", "Mid", "Senior"]
statuses = ["completed", "cancelled", "no-show"]

# Cities
for c in cities:
    cursor.execute("INSERT INTO city_master (city_name) VALUES (?)", (c,))

# Clinics
clinic_id = 1
for city_id in range(1, 6):
    for _ in range(3):
        cursor.execute("INSERT INTO clinic_master VALUES (?, ?, ?)",
                       (clinic_id, f"Clinic_{clinic_id}", city_id))
        clinic_id += 1

# Doctors
doctor_id = 1
for c_id in range(1, clinic_id):
    for _ in range(3):
        cursor.execute("INSERT INTO doctor_master VALUES (?, ?, ?, ?, ?)",
                       (
                           doctor_id,
                           f"Dr_{doctor_id}",
                           random.choice(departments),
                           random.choice(levels),
                           c_id
                       ))
        doctor_id += 1

# Patients
for i in range(1, 301):
    cursor.execute("INSERT INTO patient_master VALUES (?, ?, ?)",
                   (i, f"Patient_{i}", random.choice([0, 1])))

# Appointments
start = datetime(2024, 1, 1)

for i in range(1, 2001):
    d = start + timedelta(days=random.randint(0, 365))

    cursor.execute("""
    INSERT INTO appointment_transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        i,
        random.randint(1, 300),
        random.randint(1, doctor_id - 1),
        d.strftime("%Y-%m-%d"),
        d.strftime("%A"),
        d.month,
        random.randint(9, 20),
        random.choices(statuses, weights=[0.65, 0.15, 0.2])[0],
        random.randint(1500, 6000)
    ))

conn.commit()
conn.close()

print("✅ Database created successfully")