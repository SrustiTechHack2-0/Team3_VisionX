import cv2
import time
import streamlit as st
import numpy as np

# Import backend logic
from src.face_auth import FaceAuthSystem
from src.hazard_detector import HazardDetector
from src.access_controller import AccessController

class VideoPlayer:
    """Encapsulates the video feed and detection logic."""
    def __init__(self, face_sys: FaceAuthSystem, hazard_sys: HazardDetector, access_ctrl: AccessController):
        self.face_sys = face_sys
        self.hazard_sys = hazard_sys
        self.access_ctrl = access_ctrl
        self.cap = None

    def start_stream(self, placeholder: st.empty, status_text: st.empty):
        """
        Main loop to capture video, run detections, and update the placeholder.
        """
        self.cap = cv2.VideoCapture(0) # Default webcam
        
        if not self.cap.isOpened():
            st.error("Error: Could not open camera.")
            return

        stop_button = st.button("Stop Stream", key="stop_stream")
        
        while self.cap.isOpened() and not stop_button:
            ret, frame = self.cap.read()
            if not ret:
                st.error("Failed to read frame.")
                break
            
            # --- PROCESSING ---
            # 1. Hazard Detection (YOLO)
            detections, annotated_frame = self.hazard_sys.detect_hazards(frame)
            
            # 2. Face Recognition
            face_results = self.face_sys.recognize_faces(frame)
            final_frame = self.face_sys.draw_annotations(annotated_frame, face_results)
            
            # 3. Access Control Logic
            person_count = detections['person_count']
            status, alert = self.access_ctrl.validate_entry(person_count)
            
            # --- UI FEEDBACK ---
            # Draw Status Overlay
            color = (0, 255, 0) if "AUTHORIZED" in status else (0, 0, 255)
            cv2.putText(final_frame, f"STATUS: {status}", (20, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            
            # Draw FPS
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            # cv2.putText(final_frame, f"FPS: {int(fps)}", (final_frame.shape[1]-150, 50), 
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            # Update Streamlit Placeholder
            # Convert BGR to RGB
            final_frame_rgb = cv2.cvtColor(final_frame, cv2.COLOR_BGR2RGB)
            placeholder.image(final_frame_rgb, use_column_width=True, channels="RGB")
            
            # Update Door Status Text
            door_state = "OPEN (Auth Active)" if self.access_ctrl.check_status() else "LOCKED"
            door_color = "🟢" if "OPEN" in door_state else "🔴"
            status_text.markdown(f"**Door Status:** {door_color} {door_state}")
            
            # --- RETURN METRICS FOR DASHBOARD ---
            # We yield or return the data so the main loop can update session state
            yield {
                "detections": detections,
                "face_results": face_results,
                "status": status,
                "alert": alert
            }

            # Small sleep to allow UI responsiveness if needed (streamlit reruns loop)
            # But here we are inside a while loop, so st.rerun isn't called until we break.
            # To update sidebar metrics in real-time while video plays, this architecture is tricky.
            # Streamlit's model is script re-run.
            # Best approach for video: Run loop, update ALL UI elements inside the loop using placeholders.
            
            # time.sleep(0.03) 

        self.cap.release()
