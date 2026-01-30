import streamlit as st

def render_alert_list(alerts: list):
    """
    Renders scrollable list of recent alerts.
    
    Args:
        alerts: List of dictionary alerts from SessionManager.
    """
    st.markdown("### Recent Alerts")
    
    if not alerts:
        st.info("No alerts detected yet. System is monitoring.")
        return

    # Container with custom CSS scroll
    with st.container(height=400):
        for alert in alerts:
            timestamp_str = alert['timestamp'].strftime("%H:%M:%S")
            alert_type = alert['type']
            description = alert['description']
            
            # Icon mapping (simplified)
            icon = "ℹ️"
            if alert_type == "TAILGATING": icon = "⚠️"
            elif alert_type == "WEAPON": icon = "🔫"
            elif alert_type == "PET": icon = "🐕"
            elif alert_type == "CROWD": icon = "👥"
            elif alert_type == "UNAUTHORIZED": icon = "🚫"
            
            # Badge Color
            bg_color = "rgba(68, 136, 255, 0.2)" # Info Blue
            if alert_type in ["TAILGATING", "WEAPON", "UNAUTHORIZED"]:
                bg_color = "rgba(255, 68, 68, 0.2)" # Red
            elif alert_type == "CROWD":
                bg_color = "rgba(255, 170, 0, 0.2)" # Orange
            
            st.markdown(
                f"""
                <div style="
                    background-color: {bg_color};
                    padding: 10px;
                    border-radius: 5px;
                    margin-bottom: 8px;
                    display: flex;
                    align-items: center;
                ">
                    <span style="font-size: 1.5rem; margin-right: 15px;">{icon}</span>
                    <div>
                        <div style="font-weight: bold; font-size: 0.9em; color: #ccc;">{timestamp_str}</div>
                        <div style="font-size: 1.1em; color: white;">{description}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
