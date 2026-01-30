import streamlit as st
import cv2
import numpy as np
import time
from src.face_auth import FaceAuthSystem
from src.hazard_detector import HazardDetector
from src.access_controller import AccessController
from PIL import Image

# Page Config
st.set_page_config(page_title="SurakshaSetu Dashboard", layout="wide", page_icon="🛡️")

# UI Styling
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .main {
        background: #0e1117;
    }
    h1 { color: #00FF00; }
    .stButton>button {
        background-color: #00FF00;
        color: black;
        border-radius: 10px;
    }
    .metric-card {
        background-color: #262730;
        padding: 10px;
        border-radius: 5px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ SurakshaSetu: Intelligent Security System")
st.subheader("Real-time Unauthorized Entry & Tailgating Detection")

# Sidebar
st.sidebar.title("Control Panel")
run_system = st.sidebar.checkbox("Start System", value=False)
show_confidence = st.sidebar.checkbox("Show Model Confidence", value=False)
sim_auth = st.sidebar.button("🔑 Simulate Auth Card Swipe")

# Initialize modules (Cached to avoid reloading on every rerun)
@st.cache_resource
def load_modules():
    face_sys = FaceAuthSystem(db_path='face_db')
    hazard_sys = HazardDetector(model_path='yolov8n.pt')
    access_ctrl = AccessController()
    return face_sys, hazard_sys, access_ctrl

face_sys, hazard_sys, access_ctrl = load_modules()

# Access Trigger
if sim_auth:
    access_ctrl.trigger_access_request("Manual Button")
    st.toast("Access Granted! Window Open for 5s", icon="🔓")

# Layout
col1, col2 = st.columns([2, 1])

# Placeholders
with col1:
    st.write("### 🎥 Live Feed")
    video_placeholder = st.empty()

with col2:
    st.write("### 📊 Live Analytics")
    kpi1, kpi2 = st.columns(2)
    with kpi1:
        status_text = st.empty()
    with kpi2:
        count_text = st.empty()
    
    st.write("### 🚨 Alerts")
    alert_box = st.empty()

# Main Loop
if run_system:
    cap = cv2.VideoCapture(0) # 0 for default webcam, change if needed
    
    if not cap.isOpened():
        st.error("Error: Could not open camera.")
    else:
        while run_system:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to read from camera.")
                break
            
            # 1. Hazard Detection (YOLO)
            detections, annotated_frame = hazard_sys.detect_hazards(frame)
            
            # 2. Face Recognition
            face_results = face_sys.recognize_faces(frame)
            final_frame = face_sys.draw_annotations(annotated_frame, face_results)
            
            # 3. Access Control & Tailgating Logic
            person_count = detections['person_count']
            status, alert = access_ctrl.validate_entry(person_count)
            
            # Overlay Status on Frame
            cv2.putText(final_frame, f"STATUS: {status}", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

            # Update UI
            # Convert BGR to RGB for Streamlit
            final_frame_rgb = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(final_frame_rgb, channels="RGB", use_column_width=True)
            
            # KPIs
            if access_ctrl.check_status():
                status_text.markdown(f"**Door Status**\n\n🟢 UNLOCKED")
            else:
                status_text.markdown(f"**Door Status**\n\n🔴 LOCKED")
                
            count_text.metric("Occupants Detect", person_count)

            # Alert Logic
            alerts = []
            if detections['weapon_alert']:
                alerts.append(f"⚠️ WEAPON DETECTED: {detections['weapons']}")
            if detections['pet_alert']:
                alerts.append(f"🐾 PET DETECTED: {detections['pets']}")
            if detections['crowd_alert']:
                alerts.append(f"👥 CROWD DENSITY WARNING")
            if alert == "TAILGATING":
                alerts.append(f"🚨 TAILGATING DETECTED!")
                # Draw HUGE RED WARNING
                cv2.rectangle(final_frame, (0,0), (frame.shape[1], frame.shape[0]), (0,0,255), 10)
                
            # Unknown Face Logic (if door locked and person present)
            for name, _, _ in face_results:
                if name == "Unauthorized" and not access_ctrl.check_status():
                    alerts.append("🚫 UNAUTHORIZED PERSON")

            if alerts:
                alert_html = ""
                for a in alerts:
                    alert_html += f"<div style='padding:10px;background-color:red;color:white;margin:5px;'>{a}</div>"
                alert_box.markdown(alert_html, unsafe_allow_html=True)
            else:
                alert_box.markdown("<div style='padding:10px;background-color:green;color:white;'>✅ System Secure</div>", unsafe_allow_html=True)

            # Avoid high CPU usage
            # time.sleep(0.01) 
            
        cap.release()
else:
    st.info("Click 'Start System' in the sidebar to begin.")
