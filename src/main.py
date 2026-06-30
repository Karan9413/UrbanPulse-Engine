
import time
import os
import pandas as pd
import duckdb
import face_recognition
import pickle

DB_FILE = "urban_pulse.db"

def init_mock_databases():
    """Initializes free local DuckDB with realistic community registry data."""
    conn = duckdb.connect(DB_FILE)
    
    # Force drop stale table schemas from previous testing versions
    conn.execute("DROP TABLE IF EXISTS citizen_registry;")
    conn.execute("DROP TABLE IF EXISTS zone_risk_index;")
    
    # Re-create tables with updated structural schemas
    conn.execute("""
        CREATE TABLE citizen_registry (
            person_id VARCHAR PRIMARY KEY,
            full_name VARCHAR,
            role_profile VARCHAR,
            assigned_zone VARCHAR,
            last_seen TIMESTAMP
        );
    """)
    conn.execute("""
        CREATE TABLE zone_risk_index (
            zone_id VARCHAR,
            avg_pulse_index DOUBLE,
            total_anomalies BIGINT,
            last_updated TIMESTAMP
        );
    """)
    
    # Seed data fresh
    conn.execute("""
        INSERT INTO citizen_registry VALUES 
        ('P-001', 'Marcus Vance', 'Transit Dispatcher', 'Times Square Hub', NOW()),
        ('P-002', 'Elena Rostova', 'Emergency Response', '7th Ave Crossing', NOW()),
        ('P-003', 'Amara Diallo', 'Municipal Safety Inspector', 'Broadway Metro Station', NOW());
    """)
    conn.close()
    
def save_new_identity(person_id, name, face_image_array):
    """Encodes a face and saves the signature to DuckDB."""
    # Generate the 128-d encoding
    encodings = face_recognition.face_encodings(face_image_array)
    if not encodings:
        return False, "No face detected in image."
    
    face_encoding = pickle.dumps(encodings[0])
    
    conn = duckdb.connect(DB_FILE)
    conn.execute(
        "UPDATE citizen_registry SET face_encoding = ? WHERE person_id = ?;",
        [face_encoding, person_id]
    )
    conn.close()
    return True, "Identity encoded and saved."
# --- CRUD Operations Layer ---

def register_new_person(person_id, name, role, zone):
    """Inserts a new tracked person into the local sandbox database layer."""
    conn = duckdb.connect(DB_FILE)
    try:
        conn.execute(
            "INSERT INTO citizen_registry VALUES (?, ?, ?, ?, NOW());",
            [person_id, name, role, zone]
        )
        status = True
    except Exception:
        status = False
    conn.close()
    return status

def update_person_record(person_id, new_role, new_zone):
    """Updates profile properties for an active operator or community member."""
    conn = duckdb.connect(DB_FILE)
    conn.execute(
        "UPDATE citizen_registry SET role_profile = ?, assigned_zone = ?, last_seen = NOW() WHERE person_id = ?;",
        [new_role, new_zone, person_id]
    )
    conn.close()

def search_citizen_records(search_query):
    """Executes instant SQL pattern matching over the identity records."""
    conn = duckdb.connect(DB_FILE)
    if not search_query:
        df = conn.execute("SELECT * FROM citizen_registry ORDER BY person_id;").df()
    else:
        df = conn.execute(
            "SELECT * FROM citizen_registry WHERE LOWER(full_name) LIKE ? OR LOWER(person_id) LIKE ?;",
            [f"%{search_query.lower()}%", f"%{search_query.lower()}%"]
        ).df()
    conn.close()
    return df

def fetch_top_anomalies():
    conn = duckdb.connect(DB_FILE)
    df = conn.execute("SELECT * FROM zone_risk_index ORDER BY total_anomalies DESC;").df()
    conn.close()
    return df