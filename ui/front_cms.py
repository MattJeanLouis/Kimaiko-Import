import streamlit as st
import json
from .api_config import check_api_config

def get_available_features():
    """Determine available features based on API configuration"""
    base_features = ['Composants basiques', 'Prévisualisation', 'Export JSON']
    
    if check_api_config('openai'):
        base_features.extend(['Tous les composants', 'Suggestions IA', 'Optimisation SEO'])
    
    if check_api_config('kimaiko'):
        base_features.append('Sync Kimaiko')
    
    return base_features

def render_front_cms():
    st.title("🖥️ Front CMS")
    
    # Determine current functionality level
    current_mode = 'basic'
    if check_api_config('kimaiko') and check_api_config('openai'):
        current_mode = 'full'
    elif check_api_config('openai'):
        current_mode = 'openai'
    
    # Mode indicator and features
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
    features = get_available_features()
    
    # Display mode info and features
    st.markdown(f"""
    <div style='padding: 15px; border-radius: 5px; background-color: {info['color']}15; 
    border: 1px solid {info['color']}; margin-bottom: 20px;'>
    <h3 style='margin:0'>{info['emoji']} {info['name']}</h3>
    {info['description']}<br>
    <small>Fonctionnalités disponibles : {', '.join(features)}</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Available content types based on API configuration
    basic_types = [
        "text",
        "textMultiline",
        "container",
        "separator",
        "button-url"
    ]
    
    advanced_types = [
        "textMultiline",
        "container",
        "collection-field",
        "text",
        "icon",
        "array",
        "separator",
        "qrcode",
        "table",
        "array-child",
        "iframe",
        "fixed-iframe",
        "button-url"
    ]
    
    content_types = basic_types if not check_api_config('openai') else advanced_types
    
    # Initialize component configuration
    if 'component_config' not in st.session_state:
        st.session_state.component_config = {
            "type": "",
            "content": "",
            "showShadow": False,
            "arrayHeaderBackground": "#ffffff",
            "arrayHeaderShow": True,
            "style": {}
        }
    
    if 'ai_suggestions' not in st.session_state:
        st.session_state.ai_suggestions = None
    
    # Main content in tabs
    tab1, tab2, tab3 = st.tabs(["✏️ Configuration", "🎨 Style", "👁️ Prévisualisation"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Basic configuration
            st.subheader("📝 Configuration de base")
            
            # Component type with visual categories
            st.markdown("### Type de composant")
            component_type = st.selectbox(
                "Sélectionnez un type",
                options=content_types,
                format_func=lambda x: {
                    "text": "📝 Texte simple",
                    "textMultiline": "📄 Texte multiligne",
                    "container": "📦 Conteneur",
                    "collection-field": "🗃️ Champ de collection",
                    "icon": "🎯 Icône",
                    "array": "📋 Tableau",
                    "separator": "➖ Séparateur",
                    "qrcode": "📱 QR Code",
                    "table": "📊 Tableau",
                    "array-child": "📑 Élément de tableau",
                    "iframe": "🖼️ iFrame",
                    "fixed-iframe": "📌 iFrame fixe",
                    "button-url": "🔘 Bouton URL"
                }.get(x, x)
            )
            st.session_state.component_config["type"] = component_type
            
            # Content input based on type
            if component_type in ["text", "textMultiline"]:
                content = st.text_area(
                    "Contenu",
                    value=st.session_state.component_config.get("content", ""),
                    height=150
                )
                st.session_state.component_config["content"] = content
                
                # AI Content Suggestions (if OpenAI API is configured)
                if check_api_config('openai'):
                    if st.button("🤖 Suggestions de contenu"):
                        # Mockup AI suggestions
                        st.session_state.ai_suggestions = {
                            "content": [
                                "Découvrez notre nouvelle collection",
                                "Explorez nos services innovants",
                                "Contactez notre équipe d'experts"
                            ],
                            "style": {
                                "color": "#1a73e8",
                                "fontSize": "1.2em",
                                "fontWeight": "500"
                            }
                        }
                        st.success("✨ Suggestions générées!")
            
            # URL configuration for specific types
            if component_type in ["iframe", "fixed-iframe", "button-url"]:
                st.markdown("### Configuration URL")
                url = st.text_input(
                    "URL",
                    value=st.session_state.component_config.get("url", ""),
                    placeholder="https://..."
                )
                st.session_state.component_config["url"] = url
                
                if url and not url.startswith(('http://', 'https://')):
                    st.warning("⚠️ L'URL doit commencer par http:// ou https://")
        
        with col2:
            # AI Suggestions display
            if st.session_state.ai_suggestions:
                st.markdown("### 🤖 Suggestions IA")
                if "content" in st.session_state.ai_suggestions:
                    for suggestion in st.session_state.ai_suggestions["content"]:
                        if st.button(f"➕ {suggestion[:30]}..."):
                            st.session_state.component_config["content"] = suggestion
                            st.success("✅ Contenu appliqué!")
    
    with tab2:
        st.subheader("🎨 Options de style")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Basic style options
            st.session_state.component_config["showShadow"] = st.checkbox(
                "Ombre portée",
                value=st.session_state.component_config.get("showShadow", False)
            )
            
            if component_type == "array":
                st.session_state.component_config["arrayHeaderShow"] = st.checkbox(
                    "Afficher l'en-tête",
                    value=st.session_state.component_config.get("arrayHeaderShow", True)
                )
                st.session_state.component_config["arrayHeaderBackground"] = st.color_picker(
                    "Couleur de fond de l'en-tête",
                    value=st.session_state.component_config.get("arrayHeaderBackground", "#ffffff")
                )
            
            # Advanced style options
            st.markdown("### Style avancé")
            style = st.session_state.component_config.get("style", {})
            
            # Color
            style["color"] = st.color_picker(
                "Couleur du texte",
                value=style.get("color", "#000000")
            )
            
            # Font size
            style["fontSize"] = st.select_slider(
                "Taille du texte",
                options=["0.8em", "1em", "1.2em", "1.5em", "2em"],
                value=style.get("fontSize", "1em")
            )
            
            # Font weight
            style["fontWeight"] = st.select_slider(
                "Épaisseur du texte",
                options=["300", "400", "500", "600", "700"],
                value=style.get("fontWeight", "400")
            )
            
            st.session_state.component_config["style"] = style
        
        with col2:
            # Style preview
            st.markdown("### Aperçu du style")
            preview_style = f"""
            <div style="
                color: {style.get('color', '#000000')};
                font-size: {style.get('fontSize', '1em')};
                font-weight: {style.get('fontWeight', '400')};
                padding: 20px;
                background: white;
                border-radius: 5px;
                {f'box-shadow: 0 2px 4px rgba(0,0,0,0.1)' if st.session_state.component_config['showShadow'] else ''}
            ">
                {st.session_state.component_config.get('content', 'Exemple de texte')}
            </div>
            """
            st.markdown(preview_style, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("👁️ Prévisualisation")
        
        # Live preview based on component type
        if component_type in ["text", "textMultiline"]:
            st.markdown(preview_style, unsafe_allow_html=True)
        elif component_type == "button-url":
            url = st.session_state.component_config.get("url", "#")
            button_style = f"""
            <a href="{url}" target="_blank" style="
                display: inline-block;
                padding: 10px 20px;
                background: {style.get('color', '#1a73e8')};
                color: white;
                text-decoration: none;
                border-radius: 5px;
                font-size: {style.get('fontSize', '1em')};
                font-weight: {style.get('fontWeight', '500')};
                {f'box-shadow: 0 2px 4px rgba(0,0,0,0.1)' if st.session_state.component_config['showShadow'] else ''}
            ">
                {st.session_state.component_config.get('content', 'Cliquez ici')}
            </a>
            """
            st.markdown(button_style, unsafe_allow_html=True)
        elif component_type in ["iframe", "fixed-iframe"]:
            url = st.session_state.component_config.get("url", "")
            if url:
                st.markdown(f"""
                <iframe src="{url}" style="
                    width: 100%;
                    height: 400px;
                    border: none;
                    border-radius: 5px;
                    {f'box-shadow: 0 2px 4px rgba(0,0,0,0.1)' if st.session_state.component_config['showShadow'] else ''}
                "></iframe>
                """, unsafe_allow_html=True)
            else:
                st.info("ℹ️ Ajoutez une URL pour voir la prévisualisation")
        else:
            st.json(st.session_state.component_config)
    
    # Actions footer
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Exporter JSON", use_container_width=True):
            # Clean up configuration
            clean_config = {k: v for k, v in st.session_state.component_config.items() if v is not None}
            formatted_json = json.dumps(clean_config, indent=2)
            
            st.download_button(
                "📥 Télécharger JSON",
                data=formatted_json,
                file_name="component_config.json",
                mime="application/json"
            )
    
    with col2:
        if check_api_config('kimaiko'):
            if st.button("🔄 Synchroniser avec Kimaiko", use_container_width=True):
                # Mockup sync process
                st.info("🔄 Synchronisation avec Kimaiko...")
                st.success("✅ Composant synchronisé!")
    
    with col3:
        if st.button("🔄 Réinitialiser", use_container_width=True):
            st.session_state.component_config = {
                "type": "",
                "content": "",
                "showShadow": False,
                "arrayHeaderBackground": "#ffffff",
                "arrayHeaderShow": True,
                "style": {}
            }
            st.session_state.ai_suggestions = None
            st.rerun()
