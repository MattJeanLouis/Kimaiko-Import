# Ceci est un fichier Streamlit amélioré

import streamlit as st
import json
import pandas as pd
import io

# Assurez-vous que 'faire_requete_chatgpt' est correctement importée ou définie
from utils.manager_openai import faire_requete_chatgpt

st.title("Création de dossier Kimaiko")

def phase2_collecte_informations():
    st.header("Phase 1 : Collecte des informations")
    
    # Définition des éléments à analyser avec leur aide contextuelle
    elements_a_analyser = {
        "Mission": "La raison d'être et l'objectif principal de l'entreprise",
        "Produits et Services": "Les offres principales de l'entreprise",
        "Marché Cible": "Les clients ou segments de marché visés",
        "Avantages Concurrentiels": "Les points forts qui distinguent l'entreprise",
        "Valeurs": "Les principes fondamentaux qui guident l'entreprise"
    }

    # Champs de saisie pour le nom de l'entreprise
    entreprise = st.text_input(
        "Nom de l'entreprise",
        help="Entrez le nom légal complet de l'entreprise",
        value=st.session_state.get('entreprise', '')
    )

    # Champs de saisie multiligne pour la description détaillée de l'entreprise
    description = st.text_area(
        "Description détaillée de l'entreprise",
        help="""Veuillez fournir une description la plus complète possible incluant :
        - L'activité principale et le secteur d'activité
        - Les produits et services offerts
        - Les processus métiers clés
        - La mission et les objectifs stratégiques
        - Les valeurs fondamentales
        - Les avantages concurrentiels
        - Les marchés cibles""",
        placeholder="Décrivez votre entreprise de manière détaillée en suivant si possible les points ci-dessus...",
        value=st.session_state.get('description', '')
    )

    # Bouton pour déclencher l'analyse
    if st.button("Analyser l'entreprise"):
        if not entreprise or not description:
            st.warning("Veuillez remplir le nom et la description de l'entreprise.")
            return

        # Stocker les informations dans session_state
        st.session_state['entreprise'] = entreprise
        st.session_state['description'] = description

        # Initialiser elements_edites dans session_state
        st.session_state['elements_edites'] = {}

        elements_edites = {}

        with st.spinner("Analyse en cours..."):
            # Analyser chaque élément individuellement
            for element, aide in elements_a_analyser.items():
                prompt_element = f"""Analyse les informations suivantes et extrais uniquement l'élément demandé :

Nom de l'entreprise : {entreprise}

Description de l'entreprise :
{description}

Élément à extraire : {element}

Retourne uniquement la réponse sans texte superflu."""

                # Appeler l'API ChatGPT pour chaque élément
                resultat_element = faire_requete_chatgpt(prompt_element)

                # Sauvegarder le résultat
                if resultat_element:
                    elements_edites[element] = resultat_element.strip()
                else:
                    elements_edites[element] = ""

        # Stocker les éléments analysés dans session_state
        st.session_state['elements_edites'] = elements_edites
        st.success("Analyse terminée. Vous pouvez modifier les éléments ci-dessous.")

    # Afficher les champs d'édition si des éléments ont été analysés
    if 'elements_edites' in st.session_state and st.session_state['elements_edites']:
        st.subheader("Éléments clés de l'entreprise (modifiables)")
        elements_edites_actuels = {}

        for element, aide in elements_a_analyser.items():
            valeur = st.text_area(
                element,
                value=st.session_state['elements_edites'].get(element, ""),
                height=100,
                help=aide
            )
            elements_edites_actuels[element] = valeur

        # Mettre à jour elements_edites dans session_state avec les modifications de l'utilisateur
        st.session_state['elements_edites'] = elements_edites_actuels

def phase3_Traitement_initial_collection():
    st.header("Phase 2 : Génération des collections")

    # Vérifier que les éléments analysés existent
    if 'elements_edites' not in st.session_state or not st.session_state['elements_edites']:
        st.warning("Veuillez d'abord analyser l'entreprise dans la phase précédente.")
        return

    if 'collections_generees' not in st.session_state:
        st.session_state['collections_generees'] = []

    if st.button("Générer les collections"):
        entreprise = st.session_state.get('entreprise', '')
        description = st.session_state.get('description', '')
        elements_str = "\n".join([f"{k}: {v}" for k, v in st.session_state['elements_edites'].items()])

        with st.spinner("Génération des collections en cours..."):
            # Premier prompt pour générer les collections initiales
            prompt_collection = f"""Analyse les informations suivantes et propose une liste de collections pour un CRM :

Nom de l'entreprise : {entreprise}

Éléments analysés :
{elements_str}

Description de l'entreprise :
{description}

Format de réponse attendu (JSON) :
[
    {{"nom": "nom_collection", "description": "description_collection"}}
]

Retourne uniquement le JSON sans texte additionnel et sans les caractères ``` au début ou à la fin.
"""

            # Premier appel à l'API ChatGPT
            reponse = faire_requete_chatgpt(prompt_collection)

            try:
                # Parser la réponse JSON
                collections = json.loads(reponse)

                # Récupérer les noms des collections existantes
                noms_collections = [c["nom"] for c in collections]
                collections_str = ", ".join(noms_collections)

                # Deuxième prompt pour compléter la liste
                prompt_completion = f"""En te basant sur les informations suivantes, propose des collections ADDITIONNELLES pour compléter la liste existante pour un CRM :

Nom de l'entreprise : {entreprise}

Éléments analysés :
{elements_str}

Description de l'entreprise :
{description}

Collections déjà existantes :
{collections_str}

Format de réponse attendu (JSON) :
[
    {{"nom": "nom_collection", "description": "description_collection"}}
]

Retourne uniquement le JSON sans texte additionnel et sans les caractères ``` au début ou à la fin.
"""

                # Deuxième appel à l'API ChatGPT
                reponse_completion = faire_requete_chatgpt(prompt_completion)

                # Parser et combiner les résultats
                collections_supplementaires = json.loads(reponse_completion)
                collections_combinees = collections + collections_supplementaires

                # Troisième prompt pour analyser les relations
                prompt_relations = f"""Analyse les relations entre les collections suivantes et propose des collections supplémentaires qui pourraient servir de passerelle si nécessaire :

Collections existantes :
{json.dumps(collections_combinees, indent=2, ensure_ascii=False)}

Format de réponse attendu (JSON) :
[
    {{"nom": "nom_collection", "description": "description_collection"}}
]

Ne propose que des collections passerelles manquantes, si nécessaire.
Retourne uniquement le JSON sans texte additionnel et sans les caractères ``` au début ou à la fin.
"""

                # Troisième appel à l'API ChatGPT
                reponse_relations = faire_requete_chatgpt(prompt_relations)

                # Parser et ajouter les collections passerelles
                try:
                    collections_passerelles = json.loads(reponse_relations)
                    collections_finales = collections_combinees + collections_passerelles
                except json.JSONDecodeError:
                    collections_finales = collections_combinees

                # Supprimer les doublons
                noms_vus = set()
                collections_uniques = []
                for c in collections_finales:
                    if c['nom'] not in noms_vus:
                        noms_vus.add(c['nom'])
                        collections_uniques.append(c)

                # Sauvegarder toutes les collections
                st.session_state['collections_generees'] = collections_uniques

                st.success("Collections générées avec succès.")

            except json.JSONDecodeError:
                st.error("Erreur lors du parsing de la réponse de l'IA. Veuillez réessayer.")
                return

    # Afficher les collections si elles existent
    if 'collections_generees' in st.session_state and st.session_state['collections_generees']:
        st.subheader("Collections générées")
        df = pd.DataFrame(st.session_state['collections_generees'])
        collections_editees = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            key="collections_editables"
        )
        st.session_state['collections_generees'] = collections_editees.to_dict(orient='records')

def generer_relations_pour_collection(collection_source, toutes_collections, details_collections):
    """Génère les relations pour une collection spécifique"""
    # Simplifier le résumé des collections
    collections_resume = "\n".join([
        f"- {c['nom']}: {c['description']}"
        for c in toutes_collections
        if c['nom'] != collection_source['nom']
    ])

    prompt = f"""En tant qu'expert en modélisation de données, analyse les relations possibles depuis la collection source vers les autres collections.

Collection source:
Nom: {collection_source['nom']}
Description: {collection_source['description']}

Autres collections disponibles:
{collections_resume}

Retourne UNIQUEMENT un tableau JSON avec les relations trouvées, au format suivant:
[
    {{
        "source": "{collection_source['nom']}",
        "cible": "nom_collection_cible",
        "type_relation": "un-à-plusieurs",
        "cle_source": "id",
        "nom_cle_etrangere": "nom_suggere_cle_etrangere",
        "description": "Description courte de la relation"
    }}
]

Si aucune relation n'est trouvée, retourne un tableau vide: []"""

    try:
        # Appel API avec gestion des erreurs
        reponse = faire_requete_chatgpt(prompt)
        
        # Nettoyage de la réponse
        reponse = reponse.strip()
        if reponse.startswith('```') and reponse.endswith('```'):
            reponse = reponse[3:-3].strip()
        if reponse.startswith('json'):
            reponse = reponse[4:].strip()
            
        # Parsing JSON avec gestion des erreurs
        try:
            relations = json.loads(reponse)
            if not isinstance(relations, list):
                st.error(f"Format invalide pour {collection_source['nom']}: la réponse n'est pas un tableau")
                return []
            return relations
        except json.JSONDecodeError as e:
            st.error(f"Erreur JSON pour {collection_source['nom']}: {str(e)}\nRéponse reçue: {reponse}")
            return []
            
    except Exception as e:
        st.error(f"Erreur lors de l'analyse des relations pour {collection_source['nom']}: {str(e)}")
        return []

def verifier_et_nettoyer_relations(relations):
    """Vérifie et nettoie les relations pour éviter les doublons et incohérences"""
    relations_uniques = {}
    
    for relation in relations:
        # Créer une clé unique pour chaque paire de collections
        cle = f"{relation['source']}-{relation['cible']}"
        cle_inverse = f"{relation['cible']}-{relation['source']}"
        
        # Vérifier si la relation ou son inverse existe déjà
        if cle not in relations_uniques and cle_inverse not in relations_uniques:
            relations_uniques[cle] = relation
    
    return list(relations_uniques.values())

def phase4_collections_detail():
    st.header("Phase 3 : Détail des collections")

    # Vérifier que les collections ont été générées
    if 'collections_generees' not in st.session_state or not st.session_state['collections_generees']:
        st.warning("Veuillez d'abord générer les collections dans la phase précédente.")
        return

    if st.button("Générer les attributs détaillés pour toutes les collections"):
        if 'details_collections' not in st.session_state:
            st.session_state['details_collections'] = {}

        with st.spinner("Génération des attributs pour chaque collection..."):
            for collection in st.session_state['collections_generees']:
                nom_collection = collection['nom']

                # Vérifier si les détails existent déjà
                if nom_collection in st.session_state['details_collections']:
                    continue  # Passer si déjà généré

                # Création du prompt pour obtenir les détails d'une collection
                prompt_details = f"""
En tant qu'expert en modélisation de données, analyse la collection suivante et propose une structure détaillée des attributs :

Collection à analyser : {collection['nom']} - {collection['description']}

Génère une liste d'attributs au format CSV avec la structure suivante :
"nom_attribut","type_donnee","description","obligatoire","unique","valeur_defaut","contraintes","index"

Exemple de réponse attendue :
"nom_attribut","type_donnee","description","obligatoire","unique","valeur_defaut","contraintes","index"
"id","UUID","Identifiant unique","oui","oui","auto-généré","non null","primaire"
"date_creation","datetime","Date de création de l'enregistrement","oui","non","now()","non null","oui"

**Important :** Assure-toi que tous les champs texte, y compris ceux contenant des virgules, sont entourés de guillemets doubles, et qu'aucun champ ne contient de retour à la ligne.

Retourne uniquement le CSV avec les attributs pertinents pour cette collection, sans texte additionnel.
"""

                # Appel à l'API pour obtenir les détails
                try:
                    reponse_details = faire_requete_chatgpt(prompt_details)
                    # Nettoyer la réponse pour supprimer les espaces inutiles
                    reponse_details = reponse_details.strip()

                    # Convertir la réponse CSV en DataFrame
                    df = pd.read_csv(io.StringIO(reponse_details), delimiter=',', quotechar='"', skip_blank_lines=True)

                    # Sauvegarder les détails dans la session
                    st.session_state['details_collections'][nom_collection] = df

                except Exception as e:
                    st.error(f"Erreur lors de l'analyse des attributs pour la collection {nom_collection}: {str(e)}")
                    continue

        st.success("Attributs générés pour toutes les collections.")

    # Afficher les détails pour chaque collection
    if 'details_collections' in st.session_state and st.session_state['details_collections']:
        for collection in st.session_state['collections_generees']:
            nom_collection = collection['nom']
            if nom_collection in st.session_state['details_collections']:
                st.subheader(f"Structure de la collection : {nom_collection}")
                st.markdown(f"**Description :** {collection['description']}")

                # Afficher un tableau éditable pour les attributs
                st.subheader("Attributs (modifiables)")
                editable_df = st.data_editor(
                    st.session_state['details_collections'][nom_collection],
                    num_rows="dynamic",
                    use_container_width=True,
                    key=f"attributes_{nom_collection}"
                )

                # Mettre à jour la session avec les modifications de l'utilisateur
                st.session_state['details_collections'][nom_collection] = editable_df

    # Générer les relations entre les collections
    if st.button("Générer les relations entre les collections"):
        if 'relations_collections' not in st.session_state:
            st.session_state['relations_collections'] = []

        toutes_relations = []
        
        # Création d'un conteneur pour les messages de progression
        progress_container = st.empty()
        
        with st.spinner("Génération des relations..."):
            total_collections = len(st.session_state['collections_generees'])
            
            for idx, collection in enumerate(st.session_state['collections_generees'], 1):
                # Mise à jour du message de progression
                progress_container.info(f"Analyse de la collection {collection['nom']} ({idx}/{total_collections})")
                
                # Génération des relations pour cette collection
                relations_collection = generer_relations_pour_collection(
                    collection,
                    st.session_state['collections_generees'],
                    st.session_state['details_collections']
                )
                
                if relations_collection:
                    toutes_relations.extend(relations_collection)
            
            # Nettoyage du message de progression
            progress_container.empty()
            
            # Nettoyage et validation des relations
            if toutes_relations:
                relations_nettoyees = verifier_et_nettoyer_relations(toutes_relations)
                st.session_state['relations_collections'] = relations_nettoyees
                st.success(f"Relations générées avec succès. {len(relations_nettoyees)} relations uniques trouvées.")
                
                # Affichage des relations pour vérification
                st.write("Relations générées :")
                for relation in relations_nettoyees:
                    st.write(f"- {relation['source']} → {relation['cible']} ({relation['type_relation']})")
            else:
                st.warning("Aucune relation n'a été identifiée entre les collections.")

    # Afficher les relations si elles existent
    if 'relations_collections' in st.session_state and st.session_state['relations_collections']:
        st.subheader("Relations entre les collections")
        df_relations = pd.DataFrame(st.session_state['relations_collections'])
        # Afficher un tableau éditable pour les relations
        editable_relations = st.data_editor(
            df_relations,
            num_rows="dynamic",
            use_container_width=True,
            key="editable_relations"
        )
        # Mettre à jour la session avec les modifications de l'utilisateur
        st.session_state['relations_collections'] = editable_relations.to_dict(orient='records')

def phase5_generation_documentation():
    st.header("Phase 4 : Génération de la documentation")
    
    # Vérifier que toutes les données nécessaires sont présentes
    donnees_requises = {
        'entreprise': "les informations de l'entreprise",
        'description': "la description détaillée",
        'elements_edites': "les éléments analysés",
        'collections_generees': "les collections",
        'details_collections': "les détails des collections",
        'relations_collections': "les relations entre collections"
    }
    
    manquantes = [desc for key, desc in donnees_requises.items() if key not in st.session_state]
    
    if manquantes:
        st.warning(f"Veuillez d'abord compléter les phases précédentes. Il manque : {', '.join(manquantes)}")
        return
        
    if st.button("Générer la documentation"):
        with st.spinner("Génération de la documentation en cours..."):
            # Préparation des données pour le prompt
            elements_str = "\n".join([f"{k}: {v}" for k, v in st.session_state['elements_edites'].items()])
            collections_str = json.dumps(st.session_state['collections_generees'], indent=2, ensure_ascii=False)
            relations_str = json.dumps(st.session_state['relations_collections'], indent=2, ensure_ascii=False)
            
            # Construction du prompt pour la documentation
            prompt_doc = f"""En tant qu'expert en documentation technique, génère une documentation complète au format Markdown pour le système CRM suivant :

Entreprise : {st.session_state['entreprise']}

Description : {st.session_state['description']}

Éléments clés :
{elements_str}

Collections :
{collections_str}

Relations :
{relations_str}

Structure détaillée des collections :
"""
            # Ajouter les détails de chaque collection
            for nom, df in st.session_state['details_collections'].items():
                prompt_doc += f"\n### Collection : {nom}\n"
                prompt_doc += "```\n"
                prompt_doc += df.to_string()
                prompt_doc += "\n```\n"

            prompt_doc += "\n\nGénère une documentation technique complète au format Markdown incluant :\n"
            prompt_doc += "1. Vue d'ensemble du système\n"
            prompt_doc += "2. Architecture des données\n"
            prompt_doc += "3. Description détaillée des collections\n"
            prompt_doc += "4. Relations et dépendances\n"
            prompt_doc += "5. Contraintes et règles métier\n"
            prompt_doc += "6. Recommandations d'implémentation\n"

            # Appel à l'API pour générer la documentation
            documentation = faire_requete_chatgpt(prompt_doc)
            
            if documentation:
                st.session_state['documentation'] = documentation
                st.success("Documentation générée avec succès")
                
                # Afficher la documentation
                st.markdown(documentation)
                
                # Bouton pour télécharger la documentation
                st.download_button(
                    label="Télécharger la documentation (MD)",
                    data=documentation,
                    file_name="documentation_crm.md",
                    mime="text/markdown"
                )

# Appel des fonctions principales
phase2_collecte_informations()
phase3_Traitement_initial_collection()
phase4_collections_detail()
phase5_generation_documentation()



