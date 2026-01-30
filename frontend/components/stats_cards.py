import streamlit as st

def render_metrics(tailgating: int, weapon_count: int, pet_count: int, crowd_count: int):
    """
    Renders the metric cards row.
    
    Args:
        tailgating: Integer count of tailgating detections.
        weapon_count: Integer count of weapon detections.
        pet_count: Integer count of pet detections.
        crowd_count: Current person count from the live feed.
    """
    cols = st.columns(4)

    # 1. Tailgating Card
    with cols[0]:
        st.metric(
            label="⚠️ Tailgating Alerts", 
            value=tailgating, 
            delta="HIGH" if tailgating > 5 else "NORMAL",
            delta_color="inverse"
        )
        # st.markdown(f'<div class="metric-container">Alerts: {tailgating}</div>', unsafe_allow_html=True)

    # 2. Weapon Card
    with cols[1]:
        warn = "CRITICAL" if weapon_count > 0 else "SAFE"
        st.metric(
            label="🔫 Weapon Detections", 
            value=weapon_count,
            delta=warn,
            delta_color="inverse"
        )

    # 3. Pet Card
    with cols[2]:
        st.metric(
            label="🐕 Pet Violations", 
            value=pet_count,
            delta="Check Policy" if pet_count > 0 else None
        )

    # 4. Crowd Card
    with cols[3]:
        status_label = "NORMAL"
        if crowd_count > 5: status_label = "WARNING"
        if crowd_count > 10: status_label = "CRITICAL"
        
        st.metric(
            label="👥 Crowd Density", 
            value=crowd_count,
            delta=status_label,
            delta_color="off" if status_label == "NORMAL" else "inverse"
        )
