import streamlit as st
import pandas as pd
from pathlib import Path
import logging
from .api_config import check_api_config

def get_available_features():
    """Determine available features based on API configuration"""
    base_features = ['Import', 'Export', 'Doublons', 'Dates', 'Valeurs manquantes']
    
    if check_api_config('openai'):
        base_features.extend(['AI Suggestions', 'Auto-correction'])
    
    if check_api_config('kimaiko'):
        base_features.append('Kimaiko Sync')
    
    return base_features

def render_import_clean():
    st.title("📥 Import / Clean Data")
    
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
    
    # Initialize session state variables
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    if 'cleaned_data' not in st.session_state:
        st.session_state.cleaned_data = {}
    if 'ai_suggestions' not in st.session_state:
        st.session_state.ai_suggestions = {}
    
    # File upload section with improved UX
    st.subheader("📁 Import des fichiers")
    
    # Demo files option
    if st.checkbox("Utiliser les fichiers de démonstration"):
        st.info("🎯 Fichiers de démonstration chargés")
        # Mockup demo files
        demo_data = {
            'products': pd.DataFrame({
                'ID': range(1, 6),
                'Nom': ['Produit A', 'Produit B', 'Produit C', 'Produit D', 'Produit E'],
                'Prix': [100, 200, 150, 300, 250],
                'Date': ['2023-01-01', '2023/02/01', '01-03-2023', '2023.04.01', '01.05.2023']
            }),
            'suppliers': pd.DataFrame({
                'ID': range(1, 4),
                'Nom': ['Fournisseur X', 'Fournisseur Y', 'Fournisseur Z'],
                'Email': ['contact@x.com', None, 'contact@z.com']
            })
        }
        st.session_state.uploaded_files = demo_data
    else:
        uploaded_files = st.file_uploader(
            "Déposez vos fichiers ici",
            type=['xlsx'],
            accept_multiple_files=True,
            help="Formats acceptés: Excel (.xlsx)"
        )
        
        if uploaded_files:
            with st.spinner("Chargement des fichiers..."):
                for file in uploaded_files:
                    name = Path(file.name).stem
                    try:
                        df = pd.read_excel(file)
                        st.session_state.uploaded_files[name] = df
                        
                        with st.expander(f"📊 Données {name}"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Lignes", f"{len(df):,}")
                            with col2:
                                st.metric("Colonnes", f"{len(df.columns):,}")
                            with col3:
                                missing = df.isnull().sum().sum()
                                st.metric("Valeurs manquantes", f"{missing:,}")
                            st.dataframe(df.head(), use_container_width=True)
                    except Exception as e:
                        st.error(f"Erreur lors du chargement de {name}: {str(e)}")
                        continue
    
    # AI Suggestions (if OpenAI API is configured)
    if check_api_config('openai') and st.session_state.uploaded_files:
        st.markdown("---")
        st.subheader("🤖 Suggestions IA")
        
        if st.button("Analyser les données", use_container_width=True):
            with st.spinner("Analyse en cours..."):
                # Mockup AI suggestions
                for file_name, df in st.session_state.uploaded_files.items():
                    st.session_state.ai_suggestions[file_name] = {
                        'format_dates': ['Date'] if 'Date' in df.columns else [],
                        'standardize_names': ['Nom'] if 'Nom' in df.columns else [],
                        'missing_values': df.columns[df.isnull().any()].tolist(),
                        'anomalies': ['Prix'] if 'Prix' in df.columns else []
                    }
                st.success("✅ Analyse terminée")
    
    # Data cleaning options with improved UX
    if st.session_state.uploaded_files:
        st.markdown("---")
        st.subheader("🧹 Options de nettoyage")
        
        tabs = st.tabs([f"📄 {name}" for name in st.session_state.uploaded_files.keys()])
        for tab, (file_name, df) in zip(tabs, st.session_state.uploaded_files.items()):
            with tab:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🔍 Doublons")
                    duplicate_cols = st.multiselect(
                        "Colonnes pour la vérification",
                        options=df.columns.tolist(),
                        key=f"dup_cols_{file_name}"
                    )
                    
                    if duplicate_cols and st.button("Vérifier", key=f"check_dup_{file_name}"):
                        duplicates = df[df.duplicated(subset=duplicate_cols, keep=False)]
                        if len(duplicates) > 0:
                            st.warning(f"🔍 {len(duplicates)} doublons trouvés")
                            st.dataframe(duplicates, use_container_width=True)
                        else:
                            st.success("✅ Aucun doublon trouvé")
                
                with col2:
                    st.markdown("### 📅 Dates")
                    date_cols = st.multiselect(
                        "Colonnes de type date",
                        options=df.columns.tolist(),
                        default=st.session_state.ai_suggestions.get(file_name, {}).get('format_dates', []),
                        key=f"date_cols_{file_name}"
                    )
                    
                    if date_cols and st.button("Standardiser", key=f"std_dates_{file_name}"):
                        cleaned_df = df.copy()
                        for col in date_cols:
                            try:
                                cleaned_df[col] = pd.to_datetime(cleaned_df[col]).dt.strftime('%Y-%m-%d')
                                st.session_state.cleaned_data[file_name] = cleaned_df
                                st.success("✅ Dates standardisées")
                            except Exception as e:
                                st.error(f"Erreur: {str(e)}")
                
                st.markdown("### ❓ Valeurs manquantes")
                missing_cols = df.columns[df.isnull().any()].tolist()
                if missing_cols:
                    for col in missing_cols:
                        with st.expander(f"📊 {col} ({df[col].isnull().sum()} valeurs manquantes)"):
                            action = st.radio(
                                "Action",
                                options=["Supprimer les lignes", "Remplacer par une valeur", "Ignorer"],
                                key=f"missing_{file_name}_{col}"
                            )
                            
                            if action == "Remplacer par une valeur":
                                col1, col2 = st.columns([3, 1])
                                with col1:
                                    replacement = st.text_input(
                                        "Valeur",
                                        key=f"replace_{file_name}_{col}"
                                    )
                                with col2:
                                    if st.button("Appliquer", key=f"apply_{file_name}_{col}"):
                                        cleaned_df = df.copy()
                                        cleaned_df[col].fillna(replacement, inplace=True)
                                        st.session_state.cleaned_data[file_name] = cleaned_df
                                        st.success("✅ Appliqué")
                            
                            elif action == "Supprimer les lignes":
                                if st.button("Appliquer", key=f"apply_drop_{file_name}_{col}"):
                                    cleaned_df = df.copy()
                                    cleaned_df.dropna(subset=[col], inplace=True)
                                    st.session_state.cleaned_data[file_name] = cleaned_df
                                    st.success(f"✅ {len(df) - len(cleaned_df)} lignes supprimées")
                else:
                    st.success("✅ Aucune valeur manquante")
                
                # Kimaiko Sync (if Kimaiko API is configured)
                if check_api_config('kimaiko'):
                    st.markdown("---")
                    st.markdown("### 🔄 Synchronisation Kimaiko")
                    sync_options = st.multiselect(
                        "Options de synchronisation",
                        ['Produits', 'Prix', 'Stock', 'Fournisseurs'],
                        key=f"sync_{file_name}"
                    )
                    if sync_options and st.button("Synchroniser", key=f"sync_button_{file_name}"):
                        st.info("🔄 Synchronisation simulée avec Kimaiko")
                        st.success("✅ Données synchronisées")
    
    # Export cleaned data
    if st.session_state.cleaned_data:
        st.markdown("---")
        st.subheader("📤 Exportation")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📥 Exporter tout", use_container_width=True):
                try:
                    for name, df in st.session_state.cleaned_data.items():
                        # Create Excel writer object
                        output = pd.ExcelWriter(f"{name}_cleaned.xlsx")
                        df.to_excel(output, index=False)
                        output.close()
                        
                        # Provide download button for each file
                        with open(f"{name}_cleaned.xlsx", "rb") as f:
                            st.download_button(
                                label=f"📥 {name}_cleaned.xlsx",
                                data=f,
                                file_name=f"{name}_cleaned.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"download_{name}"
                            )
                    
                    # Display statistics
                    total_rows = sum(len(df) for df in st.session_state.cleaned_data.values())
                    st.success("✅ Export réussi!")
                    st.info(f"""
                    📊 Statistiques finales:
                    - {len(st.session_state.cleaned_data)} fichiers traités
                    - {total_rows:,} lignes au total
                    """)
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")
        
        with col2:
            if st.button("🔄 Réinitialiser", use_container_width=True):
                st.session_state.uploaded_files = {}
                st.session_state.cleaned_data = {}
                st.session_state.ai_suggestions = {}
                st.rerun()
