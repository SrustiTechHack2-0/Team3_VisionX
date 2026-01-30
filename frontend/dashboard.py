import cv2
import time
import streamlit as st
import numpy as np

# Components
from frontend.components.stats_cards import render_metrics
from frontend.components.alert_list import render_alert_list
from frontend.components.control_panel import render_control_panel
from frontend.utils.session_manager import SessionManager
from frontend.config.ui_config import COLORS

# Backend Logic
from src.face_auth import FaceAuthSystem
from src.hazard_detector import HazardDetector
from src.access_controller import AccessController

# Page Config
st.set_page_config(page_title="SurakshaSetu Dashboard", layout="wide", page_icon="🛡️")

# Load Custom CSS
with open("frontend/assets/styles.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize Session State
SessionManager.init_session()

# --- BACKEND INITIALIZATION (Cached) ---
@st.cache_resource
def load_backend():
    face_sys = FaceAuthSystem(db_path='face_db')
    hazard_sys = HazardDetector(model_path='yolov8n.pt')
    access_ctrl = AccessController()
    return face_sys, hazard_sys, access_ctrl

face_sys, hazard_sys, access_ctrl = load_backend()

# --- SIDEBAR CONTROL PANEL ---
controls = render_control_panel()

if controls['grant_access']:
    access_ctrl.trigger_access_request("Manual Button")
    st.sidebar.success("✅ Access Granted! (5s)")

# --- MAIN LAYOUT ---
st.title("🛡️ SurakshaSetu: Intelligent Security Dashboard")
st.markdown("---")

# Metrics Container (Placeholder for real-time updates)
metrics_placeholder = st.empty()

# Main Grid: Video + Alerts
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎥 Live Surveillance Feed")
    video_placeholder = st.empty()
    status_text = st.empty()

with col2:
    # Alerts container (Placeholder)
    alerts_placeholder = st.empty()

# --- MAIN LOOP ---
if controls['system_status']:
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("Error: Could not open camera.")
    else:
        st.toast("System Armed & Monitoring...", icon="🚨")
        
        while controls['system_status']:
            ret, frame = cap.read()
            if not ret:
                break
            
            # 1. Hazard Detection
            detections, annotated_frame = hazard_sys.detect_hazards(frame)
            
            # 2. Face Recognition
            face_results = face_sys.recognize_faces(frame)
            final_frame = face_sys.draw_annotations(annotated_frame, face_results)
            
            # 3. Access Control Logic
            person_count = detections['person_count']
            status, alert_msg = access_ctrl.validate_entry(person_count)
            
            # --- UPDATE STATE & ALERTS ---
            if alert_msg:
                SessionManager.add_alert('TAILGATING', alert_msg, "critical")
            
            if detections['weapon_alert']:
                SessionManager.add_alert('WEAPON', f"Detected: {detections['weapons']}", "critical")
                
            if detections['pet_alert']:
                SessionManager.add_alert('PET', f"Detected: {detections['pets']}", "warning")
                
            if detections['crowd_alert']:
                 SessionManager.add_alert('CROWD', f"High Density: {person_count}", "warning")
            
            # Check Unauthorized Faces if door locked
            unauthorized_present = False
            for name, _, _ in face_results:
                if name == "Unauthorized" and not access_ctrl.check_status():
                    unauthorized_present = True
            
            if unauthorized_present and person_count > 0:
                # Add check to prevent spamming
                pass 
                # SessionManager.add_alert('UNAUTHORIZED', "Unknown Person detected", "critical")

            # --- RENDER UPDATES ---
            
            # A. Video
            # Overlay Status
            color = (0, 255, 0) if "AUTHORIZED" in status else (0, 0, 255)
            cv2.putText(final_frame, f"STATUS: {status}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            final_frame_rgb = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)
            video_placeholder.image(final_frame_rgb, channels="RGB", use_column_width=True)
            
            # B. Status Text
            door_state = "OPEN (Auth Active)" if access_ctrl.check_status() else "LOCKED"
            status_text.markdown(f"**Door Status:** {door_state}")
            
            # C. Metrics Cards
            metrics = SessionManager.get_metrics()
            # We use the container context manager to clear and redraw metrics elegantly?
            # Actually st.metric updates in place if ID is same, but inside placeholder is better.
            with metrics_placeholder.container():
                render_metrics(
                    tailgating=metrics['tailgating_count'],
                    weapon_count=metrics['weapon_count'],
                    pet_count=metrics['pet_count'],
                    crowd_count=detections['person_count']
                )

            # D. Alert List
            alerts = SessionManager.get_alerts()
            with alerts_placeholder.container():
                render_alert_list(alerts[:7]) # Show top 7

            # Loop delay
            # time.sleep(0.01)
            
        cap.release()
else:
    st.info("System Disarmed. Use Sidebar to activate.")
