import streamlit as st

def init_standard_mode():
    """Initialize standard mode state variables"""
    if 'mappings' not in st.session_state:
        st.session_state.mappings = {}
    if 'source_files' not in st.session_state:
        st.session_state.source_files = {}

def render_standard_mode():
    """Render the standard mode interface"""
    st.title("Mode Standard")
    st.markdown("""
    ## Import de données Kimaiko
    
    Utilisez cette interface pour:
    1. Charger vos fichiers de données
    2. Configurer les mappings
    3. Valider et exporter les données
    """)
    
    # File upload section
    st.header("Chargement des fichiers")
    uploaded_file = st.file_uploader("Choisir un fichier", type=['xlsx', 'csv'])
    
    if uploaded_file is not None:
        st.session_state.source_files[uploaded_file.name] = uploaded_file
        st.success(f"Fichier {uploaded_file.name} chargé avec succès")
        
        # Mapping configuration section
        st.header("Configuration des mappings")
        if uploaded_file.name not in st.session_state.mappings:
            st.session_state.mappings[uploaded_file.name] = {}
        
        # Add mapping interface here
        st.info("Interface de mapping en cours de développement")
