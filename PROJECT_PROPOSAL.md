# Project Proposal: SurakshaSetu 🛡️
## *Smart Anti-Tailgating & Unauthorized Entry Detection System*

### 1. Concept & Innovation
**SurakshaSetu** (Security Bridge) is an AI-powered "Visual Firewall" for physical spaces. 
Traditional security relies on *Authentication* (Who has the card?), but fails at *Assurance* (Who actually entered?). 

SurakshaSetu bridges this gap by using Computer Vision to **visually verify** that the number of people entering matches the number of authorizations granted. It transforms existing dumb CCTV cameras into intelligent sentries that detect **Tailgating**, **Weapons**, and **Unauthorized intrusion** in real-time.

**Innovation Factor:**
- **Zero Hardward Cost**: Does not require expensive optical turnstiles or laser sensors. Works with standard IP cameras.
- **Privacy-First**: Can operate on "Edge" devices (local processing) without sending video streams to the cloud.
- **Multi-Threat Detection**: Combines Face Auth, Tailgating, and Weapon Detection in a single pipeline.

---

### 2. How it Works (Step-by-Step Flow)
1.  **Entry Trigger**: The system monitors an entry zone (door/gate).
2.  **Authorization Event**: A user swipes a card / scans QR (simulated in demo). The system opens a "Valid Entry Window" (e.g., 5 seconds).
3.  **Visual Verification (The AI Core)**:
    -   **Person Counting**: The camera counts how many distinct individuals cross the threshold.
    -   **Face Matching**: Checks if the face matches the ID used (if integrated) or simply flags "Unknowns".
4.  **Decision Logic**:
    -   *1 Auth + 1 Person* = ✅ **Authorized**.
    -   *1 Auth + >1 Person* = 🚨 **Tailgating Alert**.
    -   *0 Auth + 1 Person* = 🚫 **Forced Entry**.
5.  **Safety Checks**: Parallel hazard detection scans for weapons (knives/guns) or violation of policy (pets).
6.  **Response**: Real-time dashboard alert + Log event for security audit.

---

### 3. Technology Stack (The "How")
-   **Core Logic**: Python 3.13
-   **Computer Vision**:
    -   **OpenCV**: For video stream processing and basic motion analysis.
    -   **YOLOv8 (Ultralytics)**: State-of-the-art object detection for counting people and detecting weapons/pets.
    -   **DeepFace**: For facial recognition and identity verification.
-   **User Interface**: **Streamlit** (for a futuristic, responsive real-time dashboard).
-   **Deployment**: Local Edge processing (simulated on Laptop).

---

### 4. Hackathon Demonstration Strategy
We have built a fully functional prototype to demonstrate these scenarios live:

*   **Scenario A (The Good User)**: 
    *   *Action*: You click "Simulate Auth" and walk in. 
    *   *Result*: Green Box, "Authorized Entry".
*   **Scenario B (The Tailgater)**: 
    *   *Action*: You click "Simulate Auth" but walk in with a friend behind you.
    *   *Result*: **"🚨 TAILGATING DETECTED"** (System sees 1 Auth vs 2 People).
*   **Scenario C (The Intruder)**: 
    *   *Action*: You walk in *without* clicking auth.
    *   *Result*: **"🚫 UNAUTHORIZED"**.
*   **Scenario D (Hazard)**: 
    *   *Action*: Show a pair of scissors/knife.
    *   *Result*: **"⚠️ WEAPON DETECTED"**.

---

### 5. Scalability & Real-World Deployment
-   **Edge AI**: The model is optimized (YOLOv8 Nano) to run on low-cost edge devices like NVIDIA Jetson or Raspberry Pi 5 attached to each camera.
-   **Centralized Cloud Dashboard**: Multiple edge units send only metadata (alerts/logs) to a central cloud server, minimizing bandwidth usage while allowing security heads to monitor multiple gates.
-   **Integration**: Can tap into existing RTSP streams of legacy CCTV systems, upgrading them without hardware replacement.
