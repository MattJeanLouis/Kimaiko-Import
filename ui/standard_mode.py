import streamlit as st
import pandas as pd
from pathlib import Path
import logging
from utils.file_operations import generate_kimaiko_files, optimize_dataframe

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def render_standard_mode():
    """Render the standard mode interface"""
    if st.session_state.step == 1:
        st.markdown("""
        ### 📋 Étape 1: Modèles Kimaiko
        
        Commencez par importer les modèles de fichiers Kimaiko.
        Ces fichiers définissent la structure attendue pour l'import.
        """)
        
        uploaded_files = st.file_uploader(
            "Choisissez vos fichiers modèles Kimaiko (Excel)",
            type=['xlsx'],
            accept_multiple_files=True,
            key="kimaiko_upload"
        )
        
        if uploaded_files:
            with st.spinner("Chargement des modèles..."):
                st.session_state.kimaiko_templates = {}
                progress_bar = st.progress(0)
                for i, file in enumerate(uploaded_files):
                    name = Path(file.name).stem
                    try:
                        df = pd.read_excel(file)
                        st.session_state.kimaiko_templates[name] = df.columns.tolist()
                        
                        with st.expander(f"📑 Modèle {name}"):
                            st.write("Colonnes requises:")
                            for col in df.columns:
                                st.markdown(f"- {col}")
                        
                        progress_bar.progress((i + 1) / len(uploaded_files))
                    except Exception as e:
                        st.error(f"Erreur lors du chargement de {name}: {str(e)}")
                        logging.error(f"Erreur lors du chargement de {name}: {str(e)}")
                        continue
            
            if st.button("➡️ Passer aux données sources"):
                st.session_state.step = 2
                st.rerun()

    elif st.session_state.step == 2:
        st.markdown("""
        ### 📥 Étape 2: Données sources
        
        Importez maintenant vos fichiers de données sources.
        Ces sont les fichiers que vous souhaitez convertir au format Kimaiko.
        """)
        
        # Initialize uploaded files tracking if not exists
        if 'uploaded_source_files' not in st.session_state:
            st.session_state.uploaded_source_files = set()
        
        uploaded_files = st.file_uploader(
            "Choisissez vos fichiers sources (Excel)",
            type=['xlsx'],
            accept_multiple_files=True,
            key="source_upload"
        )
        
        if uploaded_files:
            current_files = {Path(file.name).stem for file in uploaded_files}
            
            # Only process files if the set of uploaded files has changed
            if current_files != st.session_state.uploaded_source_files:
                with st.spinner("Chargement des données sources..."):
                    st.session_state.source_files = {}
                    progress_bar = st.progress(0)
                    
                    for i, file in enumerate(uploaded_files):
                        name = Path(file.name).stem
                        try:
                            df = pd.read_excel(file)
                            df = optimize_dataframe(df)  # Optimize memory usage
                            
                            row_count = len(df)
                            st.session_state.source_files[name] = {
                                'columns': df.columns.tolist(),
                                'data': df,
                                'row_count': row_count
                            }
                            
                            progress_bar.progress((i + 1) / len(uploaded_files))
                            
                            with st.expander(f"📊 Données {name}"):
                                st.write(f"Nombre total de lignes: {row_count:,}")
                                st.write("Aperçu des données (5 premières lignes):")
                                st.dataframe(df.head())
                                st.write("Colonnes disponibles:")
                                for col in df.columns:
                                    st.markdown(f"- {col}")
                        except Exception as e:
                            st.error(f"Erreur lors du chargement de {name}: {str(e)}")
                            logging.error(f"Erreur lors du chargement de {name}: {str(e)}")
                            continue
                    
                    st.session_state.uploaded_source_files = current_files
            else:
                # Display existing file information
                for name, info in st.session_state.source_files.items():
                    with st.expander(f"📊 Données {name}"):
                        st.write(f"Nombre total de lignes: {info['row_count']:,}")
                        st.write("Aperçu des données (5 premières lignes):")
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
                if st.button("➡️ Configurer le mapping"):
                    st.session_state.step = 3
                    st.rerun()

    elif st.session_state.step == 3:
        st.markdown("""
        ### 🔗 Étape 3: Configuration du mapping
        """)
        
        if 'mappings' not in st.session_state:
            st.session_state.mappings = {}
            
        # Nouvelle version avec tabs et grille
        tabs = st.tabs(list(st.session_state.kimaiko_templates.keys()))
        
        for idx, (template_name, columns) in enumerate(st.session_state.kimaiko_templates.items()):
            with tabs[idx]:
                if template_name not in st.session_state.mappings:
                    st.session_state.mappings[template_name] = {"ID": {"type": "uuid"}}
                
                template_mapping = st.session_state.mappings[template_name]
                
                # Création d'une grille de 3 colonnes pour un affichage compact
                for i in range(0, len(columns), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i + j < len(columns) and columns[i + j] != "ID":
                            col = columns[i + j]
                            with cols[j]:
                                st.markdown(f"**{col}**")
                                source_file = st.selectbox(
                                    "Fichier source",
                                    options=list(st.session_state.source_files.keys()),
                                    key=f"{template_name}_{col}_file"
                                )
                                
                                if source_file:
                                    source_columns = st.session_state.source_files[source_file]['columns']
                                    source_col = st.selectbox(
                                        "Colonne source",
                                        options=source_columns,
                                        key=f"{template_name}_{col}_column"
                                    )
                                    
                                    is_ref = st.checkbox(
                                        "Référence",
                                        key=f"{template_name}_{col}_is_ref"
                                    )
                                    
                                    if is_ref:
                                        ref_model = st.selectbox(
                                            "Modèle référencé",
                                            options=list(st.session_state.kimaiko_templates.keys()),
                                            key=f"{template_name}_{col}_ref_model"
                                        )
                                        template_mapping[col] = {
                                            "source_file": source_file,
                                            "source_col": source_col,
                                            "is_ref": is_ref,
                                            "ref_model": ref_model
                                        }
                                    else:
                                        template_mapping[col] = {
                                            "source_file": source_file,
                                            "source_col": source_col,
                                            "is_ref": is_ref
                                        }

        # Generate files
        if st.button("✨ Générer et télécharger les résultats"):
            try:
                with st.spinner("Génération des fichiers en cours... Cette opération peut prendre quelques minutes pour les grands fichiers."):
                    logging.info("Début de la génération des fichiers")
                    logging.info(f"Mappings configurés: {st.session_state.mappings}")
                    
                    # Calcul des statistiques avant la génération
                    total_rows = sum(info['row_count'] for info in st.session_state.source_files.values())
                    
                    # Génération des fichiers sans les statistiques
                    zip_data = generate_kimaiko_files(st.session_state.mappings, st.session_state.source_files)
                    
                    st.success("✅ Fichiers générés avec succès!")
                    
                    # Affichage des statistiques uniquement dans l'interface
                    st.info(f"📊 Statistiques:\n- {len(st.session_state.source_files):,} fichiers traités\n- {total_rows:,} lignes au total")
                    
                    st.download_button(
                        label="📥 Télécharger le dossier des résultats",
                        data=zip_data,
                        file_name="import_kimaiko.zip",
                        mime="application/zip",
                        help="Télécharger un dossier ZIP contenant tous les fichiers générés"
                    )
            except Exception as e:
                error_msg = str(e)
                logging.error(f"Erreur lors de la génération: {error_msg}")
                
                # Display detailed error information
                st.error("Une erreur est survenue lors de la génération des fichiers:")
                st.error(error_msg)
                
                # Display technical details in an expander
                with st.expander("📝 Détails techniques"):
                    st.code(f"Message d'erreur complet:\n{error_msg}")
                    st.write("Pour résoudre ce problème:")
                    st.markdown("""
                    1. Vérifiez que tous les fichiers sources nécessaires sont chargés
                    2. Vérifiez que le mapping est correctement configuré
                    3. Assurez-vous que les colonnes référencées existent dans les fichiers sources
                    """)
        
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

def init_standard_mode():
    """Initialize standard mode"""
    st.session_state.step = 1
