import streamlit as st
import json
import re
import pandas as pd
from openai import OpenAI
from .api_config import check_api_config

def clean_json_response(response_content):
    """Nettoyer le contenu JSON pour enlever les balises Markdown"""
    cleaned_content = re.sub(r'```json|```', '', response_content).strip()
    return cleaned_content

def get_basic_info(description):
    """Get basic company information"""
    try:
        client = OpenAI(api_key=st.session_state.api_config['openai_key'])
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Analysez la description et extrayez les informations de base sur l'entreprise.
                Répondez UNIQUEMENT avec le JSON suivant:
                {
                    "basic_info": {
                        "company_name": "nom de l'entreprise",
                        "location": "localisation",
                        "industry": "secteur d'activité",
                        "main_business": "activité principale en une phrase",
                        "key_points": ["point clé 1", "point clé 2"]
                    }
                }"""},
                {"role": "user", "content": f"Analysez cette entreprise: {description}"}
            ],
            temperature=0.7
        )
        cleaned_content = clean_json_response(response.choices[0].message.content)
        st.write("Contenu nettoyé (get_basic_info):", cleaned_content)
        return json.loads(cleaned_content)
    except Exception as e:
        st.error(f"Erreur analyse basique: {str(e)}")
        return None

def analyze_activities(basic_info):
    """Analyze company activities in detail"""
    try:
        client = OpenAI(api_key=st.session_state.api_config['openai_key'])
        
        # Première étape : Analyse détaillée
        detailed_analysis = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """Analysez en profondeur les activités et besoins de l'entreprise.
                Détaillez tous les aspects :
                - Processus métier principaux
                - Documents et flux (factures, bons de commande, etc.)
                - Besoins opérationnels
                - Interactions entre services
                - Points de contrôle et validation
                - Exigences réglementaires
                Soyez le plus exhaustif possible."""},
                {"role": "user", "content": f"Analysez cette entreprise: {json.dumps(basic_info)}"}
            ],
            temperature=0.7
        )
        
        detailed_text = detailed_analysis.choices[0].message.content
        
        # Deuxième étape : Structuration en JSON
        response = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": """Structurez l'analyse en JSON selon ce format:
                {
                    "activities_analysis": {
                        "core_activities": [
                            {
                                "name": "nom de l'activité",
                                "description": "description détaillée",
                                "stakeholders": ["partie prenante 1", "partie prenante 2"],
                                "requirements": ["besoin 1", "besoin 2"]
                            }
                        ],
                        "support_activities": [
                            {
                                "name": "nom de l'activité",
                                "description": "description détaillée",
                                "importance": "importance stratégique"
                            }
                        ]
                    }
                }"""},
                {"role": "user", "content": f"Structurez cette analyse en JSON: {detailed_text}"}
            ],
            temperature=0.7
        )
        
        cleaned_content = clean_json_response(response.choices[0].message.content)
        st.write("Contenu nettoyé (analyze_activities):", cleaned_content)
        return json.loads(cleaned_content)
    except Exception as e:
        st.error(f"Erreur analyse activités: {str(e)}")
        return None

def analyze_processes(activities_analysis):
    """Analyze business processes in detail"""
    try:
        client = OpenAI(api_key=st.session_state.api_config['openai_key'])
        
        # Première étape : Analyse détaillée en texte
        detailed_analysis = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Analysez en détail les processus métier nécessaires.
                Détaillez tous les aspects :
                - Processus opérationnels
                - Étapes de chaque processus
                - Points de données nécessaires
                - Processus de gestion
                - Importance stratégique
                Soyez le plus exhaustif possible."""},
                {"role": "user", "content": f"Analysez les processus pour ces activités: {json.dumps(activities_analysis)}"}
            ],
            temperature=0.7
        )
        
        detailed_text = detailed_analysis.choices[0].message.content
        
        # Deuxième étape : Structuration en JSON
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Structurez l'analyse en JSON selon ce format:
                {
                    "processes_analysis": {
                        "operational_processes": [
                            {
                                "name": "nom du processus",
                                "description": "description détaillée",
                                "steps": ["étape 1", "étape 2"],
                                "data_points": ["donnée 1", "donnée 2"]
                            }
                        ],
                        "management_processes": [
                            {
                                "name": "nom du processus",
                                "description": "description détaillée",
                                "importance": "importance stratégique"
                            }
                        ]
                    }
                }"""},
                {"role": "user", "content": f"Structurez cette analyse en JSON: {detailed_text}"}
            ],
            temperature=0.7
        )
        
        cleaned_content = clean_json_response(response.choices[0].message.content)
        st.write("Contenu nettoyé (analyze_processes):", cleaned_content)
        return json.loads(cleaned_content)
    except Exception as e:
        st.error(f"Erreur analyse processus: {str(e)}")
        return None

def synthesize_analysis(basic_info, activities_analysis, processes_analysis):
    """Synthesize all analyses into final comprehensive analysis"""
    try:
        # Prepare a condensed version of previous analyses to save tokens
        synthesis_input = {
            "company": basic_info["basic_info"]["main_business"],
            "core_activities": [a["name"] for a in activities_analysis["activities_analysis"]["core_activities"]],
            "key_processes": [p["name"] for p in processes_analysis["processes_analysis"]["operational_processes"]]
        }
        
        # Première étape : Analyse détaillée
        client = OpenAI(api_key=st.session_state.api_config['openai_key'])
        detailed_analysis = client.chat.completions.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": """Analysez en détail et synthétisez tous les aspects de l'entreprise.
                Couvrez les points suivants:
                - Vision globale de l'entreprise
                - Activités principales
                - Processus clés
                - Besoins en données
                - Points stratégiques
                Soyez le plus exhaustif possible."""},
                {"role": "user", "content": f"Analysez ces informations: {json.dumps(synthesis_input)}"}
            ],
            temperature=0.7
        )
        
        detailed_text = detailed_analysis.choices[0].message.content
        
        # Deuxième étape : Structuration en JSON
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Structurez l'analyse en JSON selon ce format:
                {
                    "business_analysis": {
                        "company_overview": "vision synthétique de l'entreprise",
                        "main_activities": ["activité principale 1", "activité principale 2"],
                        "key_processes": ["processus clé 1", "processus clé 2"],
                        "data_needs": ["besoin en données 1", "besoin en données 2"],
                        "strategic_points": ["point stratégique 1", "point stratégique 2"]
                    }
                }"""},
                {"role": "user", "content": f"Structurez cette analyse en JSON: {detailed_text}"}
            ],
            temperature=0.7
        )
        
        cleaned_content = clean_json_response(response.choices[0].message.content)
        st.write("Contenu nettoyé (synthesize_analysis):", cleaned_content)
        return json.loads(cleaned_content)
    except Exception as e:
        st.error(f"Erreur synthèse: {str(e)}")
        return None

def get_collection_list(analysis):
    """Get a list of suggested collections from OpenAI"""
    if not check_api_config('openai'):
        return None
        
    try:
        client = OpenAI(api_key=st.session_state.api_config['openai_key'])
        
        # Première étape : Analyse détaillée
        detailed_analysis = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """Vous êtes un expert en modélisation de données. À partir de l'analyse fournie,
                analysez en détail les besoins en collections (tables) de données.
                Considérez tous les aspects :
                - Entités principales du système
                - Relations entre les entités
                - Données à stocker
                - Contraintes métier
                - Besoins en reporting
                Soyez le plus exhaustif possible."""},
                {"role": "user", "content": f"Analysez les besoins en collections pour cette analyse: {json.dumps(analysis)}"}
            ],
            temperature=0.7
        )
        
        detailed_text = detailed_analysis.choices[0].message.content
        
        # Deuxième étape : Structuration en JSON
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Structurez l'analyse en JSON selon ce format:
                {
                    "collections": [
                        {
                            "name": "nom_collection",
                            "description": "description détaillée",
                            "purpose": "objectif de cette collection",
                            "relations": ["relation avec d'autres collections"]
                        }
                    ]
                }"""},
                {"role": "user", "content": f"Structurez cette analyse en collections: {detailed_text}"}
            ],
            temperature=0.7
        )
        
        cleaned_content = clean_json_response(response.choices[0].message.content)
        st.write("Contenu nettoyé (get_collection_list):", cleaned_content)
        return json.loads(cleaned_content)
    except Exception as e:
        st.error(f"Erreur lors de la génération des collections: {str(e)}")
        return None

def get_collection_fields(collection_info):
    """Get detailed field structure for a collection from OpenAI"""
    if not check_api_config('openai'):
        return None
        
    try:
        client = OpenAI(api_key=st.session_state.api_config['openai_key'])
        
        # Première étape : Analyse détaillée
        detailed_analysis = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": """Vous êtes un expert en modélisation de données. Pour la collection décrite,
                analysez en détail les besoins en champs et leur structure.
                Considérez tous les aspects :
                - Données à stocker
                - Types de données appropriés
                - Contraintes de validation
                - Relations avec d'autres collections
                - Besoins en indexation et recherche
                Soyez le plus exhaustif possible."""},
                {"role": "user", "content": f"Analysez les besoins en champs pour cette collection: {json.dumps(collection_info)}"}
            ],
            temperature=0.7
        )
        
        detailed_text = detailed_analysis.choices[0].message.content
        
        # Deuxième étape : Structuration en JSON
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": """Structurez l'analyse en JSON selon ce format:
                {
                    "fields": [
                        {
                            "name": "nom_champ",
                            "type": "type_champ",
                            "description": "description détaillée",
                            "required": true/false,
                            "validation": "règles de validation"
                        }
                    ]
                }
                
                Types disponibles: text, number, date, boolean, url, image_url, multiline_text, currency"""},
                {"role": "user", "content": f"Structurez cette analyse en champs: {detailed_text}"}
            ],
            temperature=0.7
        )
        
        cleaned_content = clean_json_response(response.choices[0].message.content)
        st.write("Contenu nettoyé (get_collection_fields):", cleaned_content)
        return json.loads(cleaned_content)
    except Exception as e:
        st.error(f"Erreur lors de la génération des champs: {str(e)}")
        return None

def find_complementary_collections(existing_collections):
    """Affiche les collections qui ne sont pas déjà sélectionnées"""
    if not st.session_state.suggested_collections:
        return []
        
    # Obtenir les noms des collections existantes
    existing_names = [c["name"] for c in existing_collections]
    
    # Filtrer les collections suggérées qui ne sont pas déjà sélectionnées
    complementary = [
        collection for collection in st.session_state.suggested_collections 
        if collection["name"] not in existing_names
    ]
    
    return complementary

def render_conception_collection():
    st.title("🎨 Conception / Collection")
    
    # Initialize session state
    if 'analysis_step' not in st.session_state:
        st.session_state.analysis_step = 0
    if 'basic_info' not in st.session_state:
        st.session_state.basic_info = None
    if 'activities_analysis' not in st.session_state:
        st.session_state.activities_analysis = None
    if 'processes_analysis' not in st.session_state:
        st.session_state.processes_analysis = None
    if 'business_analysis' not in st.session_state:
        st.session_state.business_analysis = None
    if 'suggested_collections' not in st.session_state:
        st.session_state.suggested_collections = None
    if 'collections' not in st.session_state:
        st.session_state.collections = []
    
    # Main input section
    st.subheader("✨ Nouvelle Collection")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        instance_name = st.text_input(
            "Nom de l'instance Kimaiko",
            help="Donnez un nom à votre instance Kimaiko"
        )
        
        description = st.text_area(
            "Description des besoins",
            help="Décrivez votre entreprise et ses besoins"
        )
    
    with col2:
        if check_api_config('openai'):
            st.info("🤖 Assistant IA activé")
        else:
            st.warning("💡 Mode manuel actif")
    
    # Multi-step Analysis Process
    if description and check_api_config('openai'):
        # Step 1: Basic Information
        if st.session_state.analysis_step == 0:
            if st.button("1️⃣ Analyser les informations de base"):
                with st.spinner("Analyse des informations de base..."):
                    basic_info = get_basic_info(description)
                    if basic_info:
                        st.session_state.basic_info = basic_info
                        st.session_state.analysis_step = 1
                        st.success("✨ Informations de base analysées!")
                        st.rerun()
        
        # Display Basic Info and proceed to Step 2
        if st.session_state.analysis_step >= 1 and st.session_state.basic_info:
            with st.expander("📌 Informations de base", expanded=True):
                info = st.session_state.basic_info["basic_info"]
                st.write("Entreprise:", info["company_name"])
                st.write("Localisation:", info["location"])
                st.write("Secteur:", info["industry"])
                st.write("Activité principale:", info["main_business"])
                st.write("Points clés:", ", ".join(info["key_points"]))
                
                # Allow manual editing
                st.text_input("Modifier le nom de l'entreprise", value=info["company_name"], key="edit_company_name")
                st.text_input("Modifier la localisation", value=info["location"], key="edit_location")
                st.text_input("Modifier le secteur", value=info["industry"], key="edit_industry")
                st.text_input("Modifier l'activité principale", value=info["main_business"], key="edit_main_business")
                st.text_area("Modifier les points clés", value=", ".join(info["key_points"]), key="edit_key_points")
            
            if st.session_state.analysis_step == 1:
                if st.button("2️⃣ Analyser les activités"):
                    with st.spinner("Analyse des activités..."):
                        activities = analyze_activities(st.session_state.basic_info)
                        if activities:
                            st.session_state.activities_analysis = activities
                            st.session_state.analysis_step = 2
                            st.success("✨ Activités analysées!")
                            st.rerun()
        
        # Display Activities and proceed to Step 3
        if st.session_state.analysis_step >= 2 and st.session_state.activities_analysis:
            with st.expander("🔄 Analyse des activités", expanded=True):
                activities = st.session_state.activities_analysis["activities_analysis"]
                st.write("Activités principales:")
                for activity in activities["core_activities"]:
                    st.write(f"- {activity['name']}: {activity['description']}")
                st.write("Activités de support:")
                for activity in activities["support_activities"]:
                    st.write(f"- {activity['name']}: {activity['description']}")
                
                # Allow manual editing
                st.text_area("Modifier les activités principales", value=json.dumps(activities["core_activities"], indent=2), key="edit_core_activities")
                st.text_area("Modifier les activités de support", value=json.dumps(activities["support_activities"], indent=2), key="edit_support_activities")
            
            if st.session_state.analysis_step == 2:
                if st.button("3️⃣ Analyser les processus"):
                    with st.spinner("Analyse des processus..."):
                        processes = analyze_processes(st.session_state.activities_analysis)
                        if processes:
                            st.session_state.processes_analysis = processes
                            st.session_state.analysis_step = 3
                            st.success("✨ Processus analysés!")
                            st.rerun()
        
        # Display Processes and proceed to Final Synthesis
        if st.session_state.analysis_step >= 3 and st.session_state.processes_analysis:
            with st.expander("⚙️ Analyse des processus", expanded=True):
                processes = st.session_state.processes_analysis["processes_analysis"]
                st.write("Processus opérationnels:")
                for process in processes["operational_processes"]:
                    st.write(f"- {process['name']}: {process['description']}")
                st.write("Processus de gestion:")
                for process in processes["management_processes"]:
                    st.write(f"- {process['name']}: {process['description']}")
                
                # Allow manual editing
                st.text_area("Modifier les processus opérationnels", value=json.dumps(processes["operational_processes"], indent=2), key="edit_operational_processes")
                st.text_area("Modifier les processus de gestion", value=json.dumps(processes["management_processes"], indent=2), key="edit_management_processes")
            
            if st.session_state.analysis_step == 3:
                if st.button("4️⃣ Synthétiser l'analyse"):
                    with st.spinner("Synthèse en cours..."):
                        synthesis = synthesize_analysis(
                            st.session_state.basic_info,
                            st.session_state.activities_analysis,
                            st.session_state.processes_analysis
                        )
                        if synthesis:
                            st.session_state.business_analysis = synthesis["business_analysis"]
                            st.session_state.analysis_step = 4
                            st.success("✨ Analyse synthétisée!")
                            st.rerun()
        
        # Display Final Analysis and proceed to Collections
        if st.session_state.analysis_step >= 4 and st.session_state.business_analysis:
            with st.expander("📊 Analyse finale", expanded=True):
                analysis = st.session_state.business_analysis
                st.write("Vision globale:", analysis["company_overview"])
                st.write("Activités principales:", ", ".join(analysis["main_activities"]))
                st.write("Processus clés:", ", ".join(analysis["key_processes"]))
                st.write("Besoins en données:", ", ".join(analysis["data_needs"]))
                st.write("Points stratégiques:", ", ".join(analysis["strategic_points"]))
                
                # Allow manual editing
                st.text_area("Modifier l'analyse finale", value=json.dumps(analysis, indent=2), key="edit_final_analysis")
            
            if st.button("📋 Suggérer des collections"):
                with st.spinner("Génération des suggestions..."):
                    collections = get_collection_list(st.session_state.business_analysis)
                    if collections and 'collections' in collections:
                        st.session_state.suggested_collections = collections['collections']
                        st.success("✨ Collections suggérées!")
        
        # Display and Process Suggested Collections
        if st.session_state.suggested_collections:
            st.subheader("📚 Collections suggérées")
            
            # Afficher les collections non sélectionnées
            unselected_collections = find_complementary_collections(st.session_state.collections)
            selected_collections = st.multiselect(
                "Sélectionnez les collections à ajouter",
                options=[c['name'] for c in unselected_collections],
                default=[]
            )
            
            if st.button("Ajouter les collections sélectionnées"):
                for collection_name in selected_collections:
                    collection = next(
                        (c for c in unselected_collections if c["name"] == collection_name),
                        None
                    )
                    if collection and collection not in st.session_state.collections:
                        fields = get_collection_fields(collection)
                        if fields and 'fields' in fields:
                            new_collection = {
                                "name": collection['name'],
                                "description": collection['description'],
                                "fields": fields['fields']
                            }
                            st.session_state.collections.append(new_collection)
                            st.success(f"✨ Collection '{collection['name']}' ajoutée!")
    
    # Manual Collection Creation
    with st.expander("➕ Ajouter une collection manuellement"):
        manual_name = st.text_input("Nom de la collection à ajouter", key="manual_name")
        manual_tags = st.text_input("Tags pour la collection", key="manual_tags")
        if st.button("Ajouter la collection"):
            if manual_name:
                new_collection = {
                    "name": manual_name,
                    "description": "",
                    "fields": [],
                    "tags": manual_tags.split(",") if manual_tags else []
                }
                st.session_state.suggested_collections.append(new_collection)
                st.success(f"Collection '{manual_name}' ajoutée avec tags!")
    
    # Display Final Collections
    if st.session_state.collections:
        st.markdown("---")
        st.subheader("📚 Collections finales")
        
        for idx, collection in enumerate(st.session_state.collections):
            with st.expander(f"📑 {collection['name']}", expanded=True):
                st.write(f"Description: {collection['description']}")
                st.write(f"Tags: {', '.join(collection.get('tags', []))}")
                
                if collection['fields']:
                    data = [[f["name"], f["type"], f.get("description", ""), 
                            "Requis" if f.get("required", False) else "Optionnel",
                            f.get("validation", "")] 
                           for f in collection['fields']]
                    st.table({
                        "Nom": [d[0] for d in data],
                        "Type": [d[1] for d in data],
                        "Description": [d[2] for d in data],
                        "Statut": [d[3] for d in data],
                        "Validation": [d[4] for d in data]
                    })
                
                # New buttons for additional functionalities
                if st.button("🔄 Regénérer cette collection", key=f"regen_{idx}"):
                    # Logic to regenerate the collection
                    st.info("Regénération en cours...")
                
                if st.button("📤 Exporter en Excel", key=f"export_excel_{idx}"):
                    df = pd.DataFrame(collection['fields'])
                    df.to_excel(f"{collection['name']}.xlsx", index=False)
                    st.success("Exporté en Excel!")
                
                uploaded_excel = st.file_uploader("Importer depuis Excel", type="xlsx", key=f"import_excel_{idx}")
                if uploaded_excel:
                    df = pd.read_excel(uploaded_excel)
                    collection['fields'] = df.to_dict(orient='records')
                    st.success("Importé depuis Excel!")
                
                uploaded_json = st.file_uploader("Importer depuis JSON", type="json", key=f"import_json_{idx}")
                if uploaded_json:
                    collection_data = json.load(uploaded_json)
                    collection.update(collection_data)
                    st.success("Importé depuis JSON!")
                
                feedback = st.text_area("Feedback", key=f"feedback_{idx}")
                if st.button("Envoyer le feedback", key=f"send_feedback_{idx}"):
                    # Logic to send feedback to OpenAI
                    st.info("Feedback envoyé!")
                
                col1, col2 = st.columns([1, 4])
                with col1:
                    if st.button("🗑️ Supprimer", key=f"del_{idx}"):
                        st.session_state.collections.pop(idx)
                        st.rerun()
                
                with col2:
                    if st.button("💾 Exporter JSON", key=f"export_{idx}"):
                        st.download_button(
                            "📥 Télécharger",
                            data=json.dumps(collection, indent=2, ensure_ascii=False),
                            file_name=f"{collection['name']}.json",
                            mime="application/json",
                            key=f"download_{idx}"
                        )
    
    # Reset button
    st.markdown("---")
    if st.button("🔄 Réinitialiser tout", use_container_width=True):
        st.session_state.analysis_step = 0
        st.session_state.basic_info = None
        st.session_state.activities_analysis = None
        st.session_state.processes_analysis = None
        st.session_state.business_analysis = None
        st.session_state.suggested_collections = None
        st.session_state.collections = []
        st.rerun()
