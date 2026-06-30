"""
UrbanPulse Dashboard - Instant Browser-Side Identity Verification Portal
"""
import streamlit as st
import pandas as pd
import cv2
import numpy as np
import base64
from main import init_mock_databases, search_citizen_records, register_new_person, update_person_record

# Initialize database environment
init_mock_databases()

st.set_page_config(page_title="UrbanPulse Admin Hub", layout="wide", page_icon="🌐")
st.title("🌐 UrbanPulse AI: Identity Management & Mobility Analytics")
st.markdown("### Track 1 Prototype: AI for Better Living and Smarter Communities")
st.write("---")

# Main Interface Tab Navigation
tab_analytics, tab_search, tab_register, tab_update = st.tabs([
    "🎥 Live Browser Vision", 
    "🔍 Search Personnel", 
    "➕ Register New Person", 
    "📝 Update Details"
])

# --- TAB 1: BROWSER WEBCAM STREAM ---
with tab_analytics:
    st.header("📸 Real-Time Edge Video Node")
    st.markdown("Capture a live frame from your local camera to check against the DuckDB registry:")
    
    # Native Streamlit Browser Camera Component (Bypasses network lag entirely)
    img_file_buffer = st.camera_input("Take a snapshot to verify identity matrix")

    if img_file_buffer is not None:
        # 1. Convert to RGB (required by face_recognition)
        img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # 2. Get face locations and encodings from current frame
        face_locations = face_recognition.face_locations(rgb_img)
        face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
        
        # 3. Match against Database (Fetch all registered encodings)
        conn = duckdb.connect(DB_FILE)
        known_people = conn.execute("SELECT person_id, full_name, face_encoding FROM citizen_registry WHERE face_encoding IS NOT NULL;").fetchall()
        conn.close()
        
        for (top, right, bottom, left), face_enc in zip(face_locations, face_encodings):
            # Draw box
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            
            # Compare with DB
            match_name = "Unknown"
            for p_id, name, enc_blob in known_people:
                known_enc = pickle.loads(enc_blob)
                if face_recognition.compare_faces([known_enc], face_enc)[0]:
                    match_name = name
                    break
            
            # Overlay name
            cv2.putText(img, match_name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        st.image(img, channels="BGR")

# --- TAB 2: SEARCH PERSONNEL ---
with tab_search:
    st.header("🔍 Citizen & Personnel Search Engine")
    search_term = st.text_input("Enter name or Person ID to query database matrix:", placeholder="e.g., Marcus", key="search_bar")
    
    records_df = search_citizen_records(search_term)
    if records_df.empty:
        st.warning("No tracking profiles match the search parameters.")
    else:
        st.dataframe(records_df, use_container_width=True, hide_index=True)

# --- TAB 3: REGISTER NEW PERSON ---
with tab_register:
    st.header("➕ Register New Transit Profile")
    with st.form("registration_form"):
        new_id = st.text_input("Unique Person ID Code (Format: P-XXX):")
        new_name = st.text_input("Full Name:")
        new_role = st.selectbox("Role Assignment Profile:", ["Transit Commuter", "Station Dispatcher", "Municipal Maintenance", "Emergency Services"])
        new_zone = st.selectbox("Assigned Primary Monitoring Node:", ["Times Square Hub", "7th Ave Crossing", "Broadway Metro Station", "Grand Central Terminal"])
        
        submit_btn = st.form_submit_button("💾 Save Profile Registry to Database")
        if submit_btn:
            if not new_id or not new_name:
                st.error("Submission failed: Unique Person ID and Full Name are mandatory fields.")
            else:
                success = register_new_person(new_id, new_name, new_role, new_zone)
                if success:
                    st.success(f"Identity Record for {new_name} successfully initialized inside DuckDB.")
                else:
                    st.error("Error: Person ID conflict. This identifier already exists inside the structural ledger.")

# --- TAB 4: UPDATE DETAILS ---
with tab_update:
    st.header("📝 Modify Existing Operator Parameters")
    all_current = search_citizen_records("")
    if all_current.empty:
        st.info("No active registry rows available to modify.")
    else:
        target_person = st.selectbox("Select Target Profile to Modify:", all_current['person_id'] + " - " + all_current['full_name'])
        target_id = target_person.split(" - ")[0]
        
        with st.form("update_form"):
            updated_role = st.selectbox("Update Role Assignment Profile:", ["Transit Commuter", "Station Dispatcher", "Municipal Maintenance", "Emergency Services"])
            updated_zone = st.selectbox("Update Assigned Primary Monitoring Node:", ["Times Square Hub", "7th Ave Crossing", "Broadway Metro Station", "Grand Central Terminal"])
            
            update_btn = st.form_submit_button("⚡ Execute Database Record Update")
            if update_btn:
                update_person_record(target_id, updated_role, updated_zone)
                st.success(f"Database Record for Profile {target_id} updated and synchronized.")