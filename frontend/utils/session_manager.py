import streamlit as st
import datetime
import pandas as pd
from typing import List, Dict, Any

class SessionManager:
    """Manages the application state and session variables."""

    @staticmethod
    def init_session():
        """Initialize all session state variables."""
        if 'alerts' not in st.session_state:
            st.session_state['alerts'] = []
        
        if 'metrics' not in st.session_state:
            st.session_state['metrics'] = {
                'tailgating_count': 0,
                'weapon_count': 0,
                'pet_count': 0,
                'crowd_count': 0,
                'unauthorized_count': 0
            }
            
        if 'last_update' not in st.session_state:
            st.session_state['last_update'] = datetime.datetime.now()
            
        if 'system_status' not in st.session_state:
            st.session_state['system_status'] = "ACTIVE"

    @staticmethod
    def add_alert(alert_type: str, description: str, severity: str = "warning"):
        """Add a new alert to the session history."""
        timestamp = datetime.datetime.now()
        
        # Avoid duplicate alerts in short timeframe (debounce logic optional, here simplified)
        # Check last alert
        if st.session_state['alerts']:
            last_alert = st.session_state['alerts'][0]
            time_diff = (timestamp - last_alert['timestamp']).total_seconds()
            if last_alert['type'] == alert_type and time_diff < 2.0:
                return # Skip duplicate

        new_alert = {
            "timestamp": timestamp,
            "type": alert_type,
            "description": description,
            "severity": severity
        }
        
        # Insert at beginning
        st.session_state['alerts'].insert(0, new_alert)
        
        # Update metrics
        key = f"{alert_type.lower()}_count"
        # Map alert type to metric key if needed, or just follow conversation convention
        if alert_type == "TAILGATING": st.session_state['metrics']['tailgating_count'] += 1
        elif alert_type == "WEAPON": st.session_state['metrics']['weapon_count'] += 1
        elif alert_type == "PET": st.session_state['metrics']['pet_count'] += 1
        elif alert_type == "CROWD": st.session_state['metrics']['crowd_count'] += 1 # Crowd is instantaneous usually, but count alerts
        elif alert_type == "UNAUTHORIZED": st.session_state['metrics']['unauthorized_count'] += 1

        # Keep only last 100 alerts
        if len(st.session_state['alerts']) > 100:
             st.session_state['alerts'].pop()

    @staticmethod
    def get_alerts() -> List[Dict[str, Any]]:
        return st.session_state['alerts']

    @staticmethod
    def get_metrics() -> Dict[str, int]:
        return st.session_state['metrics']
