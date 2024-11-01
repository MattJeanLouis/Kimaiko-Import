import streamlit as st
from pathlib import Path
from utils.file_operations import load_demo_files, generate_kimaiko_files
from utils.demo_config import DEFAULT_MAPPINGS, DEMO_DESCRIPTIONS

def render_demo_mode():
    """Render the demo mode interface"""
    if st.session_state.step == 1:
        st.markdown(DEMO_DESCRIPTIONS["templates"])
        
        for name, columns in st.session_state.kimaiko_templates.items():
            with st.expander(f"📑 Modèle {name}"):
                st.write("Colonnes requises:")
                for col in columns:
                    st.markdown(f"- {col}")
        
        if st.button("➡️ Voir les données sources"):
            st.session_state.step = 2
            st.rerun()

    elif st.session_state.step == 2:
        st.markdown(DEMO_DESCRIPTIONS["source_files"])
        
        for name, info in st.session_state.source_files.items():
            with st.expander(f"📊 Données {name}"):
                st.write("Aperçu des données:")
                st.dataframe(info['data'].head())
                st.write("Colonnes disponibles:")
                for col in info['columns']:
                    st.markdown(f"- {col}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Retour aux modèles"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("➡️ Voir le mapping"):
                st.session_state.step = 3
                st.rerun()

    elif st.session_state.step == 3:
        st.markdown(DEMO_DESCRIPTIONS["mapping"])
        
        # Display mapping for each model
        for template_name, mappings in st.session_state.mappings.items():
            with st.expander(f"🔍 Mapping pour {template_name}"):
                st.write("Configuration du mapping:")
                for col, mapping in mappings.items():
                    if mapping.get('type') == 'uuid':
                        st.markdown(f"- **{col}** : Généré automatiquement (UUID)")
                    elif mapping.get('is_ref'):
                        st.markdown(f"- **{col}** : {mapping['source_file']}.{mapping['source_col']} (avec UUID de {mapping['ref_model']})")
                    else:
                        st.markdown(f"- **{col}** : {mapping['source_file']}.{mapping['source_col']}")
        
        # File generation
        if st.button("✨ Générer et télécharger les résultats"):
            with st.spinner("Génération des fichiers en cours..."):
                zip_data = generate_kimaiko_files(st.session_state.mappings, st.session_state.source_files)
                
                st.success("✅ Fichiers générés avec succès!")
                
                st.download_button(
                    label="📥 Télécharger le dossier des résultats",
                    data=zip_data,
                    file_name="import_kimaiko.zip",
                    mime="application/zip",
                    help="Télécharger un dossier ZIP contenant tous les fichiers générés"
                )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬅️ Retour aux données sources"):
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.button("🔄 Recommencer"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

def init_demo_mode():
    """Initialize demo mode with sample data"""
    demo_dir = Path("demo_files")
    kimaiko_templates, source_files = load_demo_files(demo_dir)
    
    st.session_state.kimaiko_templates = kimaiko_templates
    st.session_state.source_files = source_files
    st.session_state.mappings = DEFAULT_MAPPINGS
    st.session_state.step = 1
