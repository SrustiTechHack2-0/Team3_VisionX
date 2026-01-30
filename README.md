# SurakshaSetu 🛡️
**AI-Powered Unauthorized Entry & Tailgating Detection System**

## Quick Start (Hackathon Mode)

### 1. Setup
Make sure you have the dependencies installed:
```bash
pip install -r requirements.txt
```

### 2. Add Authorized Faces
1. Go to the `face_db` folder.
2. Add clear **JPEG/PNG** images of "Authorized" people.
3. **Rename the files** to the person's name (e.g., `Rahul_Sharma.jpg`).

### 3. Run the Dashboard
Double-click **`run_suraksha.bat`** or run:
```bash
python -m streamlit run frontend/dashboard.py
```

---

## 🎮 Dashboard Guide

### **Live Monitoring Panel**
- **Video Feed**: Shows real-time detection with overlays.
  - **Green Box**: Authorized Person.
  - **Red Box**: Unknown / Unauthorized.
  - **Yellow/Orange**: Weapons or Pets detected.
- **Metrics**: 4 Cards showing Total Alerts for Tailgating, Weapons, Pets, and Crowd Density.

### **Control Panel (Sidebar)**
- **🔓 Simulate Access Grant**: Click this to "Open the Door" virtually for 5 seconds.
- **🔧 Settings**: Toggle specific detection modules (e.g., turn off Weapon Detection if false positives occur).
- **🧠 AI Parameters**: Adjust confidence threshold.
- **⚠️ Reset System**: Clear all logs and counters.

### **Alerts Section**
- A scrollable list of recent security events with timestamps and severity indicators.

---

## 🏗️ Architecture
- **`frontend/dashboard.py`**: The main application entry point.
- **`frontend/components/`**: Modular UI components (Video Player, Stats Cards, Alert List).
- **`src/`**: Backend AI logic (Face Auth, YOLOv8, Access Control).
