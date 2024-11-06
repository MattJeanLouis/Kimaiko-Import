import streamlit as st

def check_api_config(api_type):
    """Check if API configuration is valid"""
    if api_type == 'openai':
        return (
            'api_config' in st.session_state and
            st.session_state.api_config.get('openai_key', '').startswith('sk-')
        )
    elif api_type == 'kimaiko':
        config = st.session_state.get('api_config', {})
        return all([
            config.get('kimaiko_url', '').startswith(('http://', 'https://')),
            config.get('kimaiko_user', ''),
            config.get('kimaiko_password', '')
        ])
    return False

def render_api_config():
    st.title("⚙️ Configuration des API")
    
    # Initialize session state for API configurations
    if 'api_config' not in st.session_state:
        st.session_state.api_config = {
            'openai_key': '',
            'kimaiko_url': '',
            'kimaiko_user': '',
            'kimaiko_password': ''
        }
    
    # Current functionality level
    current_mode = 'basic'
    if check_api_config('kimaiko') and check_api_config('openai'):
        current_mode = 'full'
    elif check_api_config('openai'):
        current_mode = 'openai'
    
    # Mode status display
    mode_info = {
        'basic': {
            'color': 'blue',
            'emoji': '🌱',
            'name': 'Basic',
            'description': 'Mode sans API - Fonctionnalités de base disponibles'
        },
        'openai': {
            'color': 'orange',
            'emoji': '🤖',
            'name': 'OpenAI',
            'description': 'Mode avec IA - Fonctionnalités avancées de traitement'
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
    <div style='padding: 15px; border-radius: 5px; background-color: {info['color']}15; 
    border: 1px solid {info['color']}; margin-bottom: 20px;'>
    <h3 style='margin:0'>{info['emoji']} Fonctionnalités actives : {info['name']}</h3>
    {info['description']}
    </div>
    """, unsafe_allow_html=True)
    
    # OpenAI Configuration
    st.subheader("🤖 Configuration OpenAI")
    
    # Help expander for OpenAI API
    with st.expander("ℹ️ Comment obtenir une clé API OpenAI ?"):
        st.markdown("""
        1. Visitez [OpenAI API](https://platform.openai.com/signup)
        2. Créez un compte ou connectez-vous
        3. Accédez à la section API Keys
        4. Cliquez sur "Create new secret key"
        5. Copiez la clé et collez-la ci-dessous
        """)
    
    openai_key = st.text_input(
        "Clé API OpenAI",
        value=st.session_state.api_config['openai_key'],
        type="password",
        help="Votre clé API OpenAI pour l'accès aux services d'intelligence artificielle",
        placeholder="sk-..."
    )
    
    if openai_key:
        if openai_key.startswith('sk-'):
            st.session_state.api_config['openai_key'] = openai_key
            st.success("✅ Clé OpenAI valide - Fonctionnalités IA débloquées")
        else:
            st.error("❌ Format de clé OpenAI invalide. La clé doit commencer par 'sk-'")
    
    # Kimaiko Configuration
    st.markdown("---")
    st.subheader("🔑 Configuration Kimaiko")
    
    # Help expander for Kimaiko API
    with st.expander("ℹ️ Configuration Kimaiko"):
        st.markdown("""
        Pour configurer l'accès à l'API Kimaiko, vous aurez besoin de :
        1. L'URL de l'API Kimaiko
        2. Vos identifiants de connexion
        
        Contactez votre administrateur si vous n'avez pas ces informations.
        """)
    
    # API URL with validation
    kimaiko_url = st.text_input(
        "URL de l'API Kimaiko",
        value=st.session_state.api_config['kimaiko_url'],
        help="L'URL de base de l'API Kimaiko",
        placeholder="https://api.kimaiko.com"
    )
    
    if kimaiko_url:
        if kimaiko_url.startswith(('http://', 'https://')):
            st.session_state.api_config['kimaiko_url'] = kimaiko_url
            st.success("✅ Format d'URL valide")
        else:
            st.error("❌ L'URL doit commencer par http:// ou https://")
    
    # Authentication in columns
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.api_config['kimaiko_user'] = st.text_input(
            "Utilisateur Kimaiko",
            value=st.session_state.api_config['kimaiko_user'],
            placeholder="votre-utilisateur"
        )
    
    with col2:
        st.session_state.api_config['kimaiko_password'] = st.text_input(
            "Mot de passe Kimaiko",
            value=st.session_state.api_config['kimaiko_password'],
            type="password",
            placeholder="••••••••"
        )
    
    st.markdown("---")
    
    # Save configuration
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("💾 Sauvegarder", use_container_width=True):
            st.success("✅ Configuration sauvegardée")
            
            # Display current functionality level
            if check_api_config('kimaiko') and check_api_config('openai'):
                st.info("⭐ Toutes les fonctionnalités sont débloquées!")
            elif check_api_config('openai'):
                st.info("🤖 Fonctionnalités IA débloquées")
            else:
                st.info("🌱 Mode basic actif")
    
    with col2:
        if st.button("🔄 Réinitialiser", use_container_width=True):
            st.session_state.api_config = {
                'openai_key': '',
                'kimaiko_url': '',
                'kimaiko_user': '',
                'kimaiko_password': ''
            }
            st.rerun()
