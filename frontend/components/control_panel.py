import streamlit as st

def render_control_panel():
    """
    Renders sidebar control panel for settings and interactions.
    """
    st.sidebar.title("⚙️ Control Panel")
    st.sidebar.markdown("---")
    
    # 1. Access Actions
    st.sidebar.header("🚪 Access Control")
    grant_access = st.sidebar.button("🔓 Simulate Access Grant\n(Open Door)", type="primary", use_container_width=True)
    
    st.sidebar.markdown("---")
    
    # 2. System Settings
    st.sidebar.header("🔧 Settings")
    system_status = st.sidebar.toggle("System Armed", value=True)
    
    enable_tailgating = st.sidebar.checkbox("Enable Tailgating Detection", value=True)
    enable_weapon = st.sidebar.checkbox("Enable Weapon Detection", value=True)
    enable_pet = st.sidebar.checkbox("Enable Pet Detection", value=True)
    enable_crowd = st.sidebar.checkbox("Enable Crowd Monitoring", value=True)
    
    st.sidebar.markdown("---")
    
    # 3. Model Params
    st.sidebar.header("🧠 AI Parameters")
    confidence = st.sidebar.slider("Confidence Threshold", 0.3, 0.9, 0.5, 0.1)
    
    # 4. Register User
    st.sidebar.markdown("---")
    st.sidebar.header("👤 Register New User")
    
    with st.sidebar.expander("Add Authorized Person"):
        new_name = st.text_input("Name")
        register_img = st.camera_input("Take Photo", key="reg_cam")
        
        if st.button("Save Profile", type="primary"):
            if new_name and register_img:
                import os
                # Save Image
                if not os.path.exists("face_db"):
                    os.makedirs("face_db")
                
                file_path = os.path.join("face_db", f"{new_name}.jpg")
                with open(file_path, "wb") as f:
                    f.write(register_img.getbuffer())
                
                st.sidebar.success(f"Registered: {new_name}")
                # Clear cache so system reloads the new user
                st.cache_resource.clear()
                # Optional: Force rerun to reload backend immediately
                # st.rerun() 
            else:
                st.sidebar.error("Name & Photo required!")

    st.sidebar.markdown("---")
    
    # 5. Actions
    if st.sidebar.button("⚠️ Reset System State", type="secondary", key="reset_sys"):
        st.cache_data.clear()
        st.session_state['alerts'] = []
        metrics_keys = ['tailgating_count', 'weapon_count', 'pet_count', 'crowd_count', 'unauthorized_count']
        for k in metrics_keys:
             st.session_state['metrics'][k] = 0
        st.rerun()

    return {
        "grant_access": grant_access,
        "system_status": system_status,
        "features": {
            "tailgating": enable_tailgating,
            "weapon": enable_weapon,
            "pet": enable_pet,
            "crowd": enable_crowd
        },
        "confidence": confidence
    }
