import streamlit as st
from ui.conception_collection import render_conception_collection
from ui.front_cms import render_front_cms
from ui.import_clean import render_import_clean
from ui.api_config import render_api_config, check_api_config
from utils.demo_config import HELP_DESCRIPTIONS

# Configure Streamlit page
st.set_page_config(
    page_title="Kimaiko",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'current_module' not in st.session_state:
    st.session_state.current_module = 'home'
if 'step' not in st.session_state:
    st.session_state.step = 0
if 'kimaiko_templates' not in st.session_state:
    st.session_state.kimaiko_templates = {}
if 'source_files' not in st.session_state:
    st.session_state.source_files = {}
if 'mappings' not in st.session_state:
    st.session_state.mappings = {}
if 'api_config' not in st.session_state:
    st.session_state.api_config = {
        'openai_key': '',
        'kimaiko_url': '',
        'kimaiko_user': '',
        'kimaiko_password': ''
    }

def render_home():
    st.title("🔄 Kimaiko")
    
    # Determine current functionality level
    current_mode = 'basic'
    if check_api_config('kimaiko') and check_api_config('openai'):
        current_mode = 'full'
    elif check_api_config('openai'):
        current_mode = 'openai'
    
    # Mode indicator
    mode_info = {
        'basic': {
            'color': 'blue',
            'emoji': '🌱',
            'name': 'Basic',
            'description': 'Fonctionnalités de base disponibles'
        },
        'openai': {
            'color': 'orange',
            'emoji': '🤖',
            'name': 'OpenAI',
            'description': 'Fonctionnalités IA activées'
        },
        'full': {
            'color': 'green',
            'emoji': '⭐',
            'name': 'Complet',
            'description': 'Toutes les fonctionnalités disponibles'
        }
    }
    
    info = mode_info[current_mode]
    st.markdown(f"""
    <div style='padding: 10px; border-radius: 5px; background-color: {info['color']}15; 
    border: 1px solid {info['color']}; margin-bottom: 20px;'>
    <h3 style='margin:0'>{info['emoji']} {info['name']}</h3>
    {info['description']}
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message
    st.markdown(HELP_DESCRIPTIONS["welcome"])
    
    st.markdown("""
    ### Modules disponibles
    
    Choisissez un module pour commencer :
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        ### 🎨 Conception / Collection
        
        Créez et configurez vos collections personnalisées
        """)
        if st.button("Conception / Collection", key="home_conception"):
            st.session_state.current_module = 'conception'
            st.rerun()
    
    with col2:
        st.info("""
        ### 🖥️ Front CMS
        
        Configurez les composants visuels
        """)
        if st.button("Front CMS", key="home_front_cms"):
            st.session_state.current_module = 'front_cms'
            st.rerun()
    
    with col3:
        st.info("""
        ### 📥 Import / Clean Data
        
        Importez et nettoyez vos données
        """)
        if st.button("Import / Clean Data", key="home_import_clean"):
            st.session_state.current_module = 'import_clean'
            st.rerun()

def main():
    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        
        # Mode indicator in sidebar
        current_mode = 'basic'
        if check_api_config('kimaiko') and check_api_config('openai'):
            current_mode = 'full'
        elif check_api_config('openai'):
            current_mode = 'openai'
        
        mode_emoji = {'basic': '🌱', 'openai': '🤖', 'full': '⭐'}
        mode_names = {'basic': 'Basic', 'openai': 'OpenAI', 'full': 'Complet'}
        st.markdown(f"**{mode_emoji[current_mode]} Fonctionnalités {mode_names[current_mode]}**")
        
        st.markdown("---")
        
        if st.button("🏠 Accueil", key="sidebar_home"):
            st.session_state.current_module = 'home'
            st.rerun()
        
        st.markdown("### Modules")
        
        if st.button("🎨 Conception / Collection", key="sidebar_conception"):
            st.session_state.current_module = 'conception'
            st.rerun()
        
        if st.button("🖥️ Front CMS", key="sidebar_front_cms"):
            st.session_state.current_module = 'front_cms'
            st.rerun()
        
        if st.button("📥 Import / Clean Data", key="sidebar_import_clean"):
            st.session_state.current_module = 'import_clean'
            st.rerun()
        
        st.markdown("---")
        
        if st.button("⚙️ Configuration des API", key="sidebar_api_config"):
            st.session_state.current_module = 'api_config'
            st.rerun()
        
        # Help section in sidebar
        st.markdown("---")
        with st.expander("ℹ️ Aide"):
            st.markdown("""
            **Niveaux de fonctionnalités:**
            - 🌱 **Basic**: Interface de base
            - 🤖 **OpenAI**: Fonctionnalités IA
            - ⭐ **Complet**: Toutes les fonctionnalités
            
            Les fonctionnalités sont automatiquement 
            activées selon votre configuration API.
            """)
    
    # Main content area
    if st.session_state.current_module == 'home':
        render_home()
    
    elif st.session_state.current_module == 'conception':
        render_conception_collection()
    
    elif st.session_state.current_module == 'front_cms':
        render_front_cms()
    
    elif st.session_state.current_module == 'import_clean':
        render_import_clean()
    
    elif st.session_state.current_module == 'api_config':
        render_api_config()

if __name__ == "__main__":
    main()
