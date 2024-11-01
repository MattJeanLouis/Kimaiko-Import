import streamlit as st
from ui.demo_mode import render_demo_mode, init_demo_mode
from ui.standard_mode import render_standard_mode, init_standard_mode
from utils.demo_config import DEMO_DESCRIPTIONS

# Configure Streamlit page
st.set_page_config(
    page_title="Import Kimaiko",
    page_icon="📊",
    layout="wide"
)

# Initialize session state
if 'mode' not in st.session_state:
    st.session_state.mode = None
if 'step' not in st.session_state:
    st.session_state.step = 0  # 0 = mode selection
if 'kimaiko_templates' not in st.session_state:
    st.session_state.kimaiko_templates = {}
if 'source_files' not in st.session_state:
    st.session_state.source_files = {}
if 'mappings' not in st.session_state:
    st.session_state.mappings = {}

def main():
    st.title("🔄 Assistant d'Import Kimaiko")
    
    # Mode selection (step 0)
    if st.session_state.step == 0:
        st.markdown(DEMO_DESCRIPTIONS["welcome"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            ### 🎮 Mode Démonstration
            
            - Utilise des données d'exemple pré-configurées
            - Guide pas à pas avec explications détaillées
            - Parfait pour comprendre le fonctionnement
            """)
            if st.button("📚 Démarrer la Démo", help="Utiliser des données d'exemple"):
                st.session_state.mode = "demo"
                init_demo_mode()
                st.rerun()
        
        with col2:
            st.info("""
            ### 💼 Mode Standard
            
            - Importez vos propres fichiers
            - Configurez votre mapping personnalisé
            - Pour l'utilisation réelle
            """)
            if st.button("🔧 Mode Standard", help="Utiliser vos propres fichiers"):
                st.session_state.mode = "standard"
                init_standard_mode()
                st.rerun()
    
    # Display progress for steps > 0
    elif st.session_state.step > 0:
        progress_text = {
            1: "📋 Étape 1: Modèles Kimaiko",
            2: "📁 Étape 2: Données sources",
            3: "🔗 Étape 3: Mapping et génération"
        }
        
        st.progress((st.session_state.step - 1) / 3)
        st.header(progress_text[st.session_state.step])
        
        if st.session_state.mode == "demo":
            st.info(DEMO_DESCRIPTIONS["demo_mode"])
            render_demo_mode()
        else:
            render_standard_mode()

if __name__ == "__main__":
    main()
