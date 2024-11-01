DEFAULT_MAPPINGS = {
    "Fournisseurs": {
        "ID": {"type": "uuid"},
        "Nom": {"source_file": "Ancien Fournisseurs", "source_col": "RaisonSociale"},
        "Email": {"source_file": "Ancien Fournisseurs", "source_col": "ContactEmail"},
        "Telephone": {"source_file": "Ancien Fournisseurs", "source_col": "NumeroTel"},
        "Adresse": {"source_file": "Ancien Fournisseurs", "source_col": "AdresseComplete"}
    },
    "Articles": {
        "ID": {"type": "uuid"},
        "Reference": {"source_file": "Ancien Articles", "source_col": "CodeArticle"},
        "Nom": {"source_file": "Ancien Articles", "source_col": "Designation"},
        "Prix": {"source_file": "Ancien Articles", "source_col": "PrixUnitaire"},
        "ID_Fournisseur": {
            "source_file": "Ancien Articles",
            "source_col": "CodeFournisseur",
            "is_ref": True,
            "ref_model": "Fournisseurs",
            "ref_key": "Code"
        }
    },
    "Factures": {
        "ID": {"type": "uuid"},
        "Numero": {"source_file": "Ancien Factures", "source_col": "NumeroFacture"},
        "Date": {"source_file": "Ancien Factures", "source_col": "DateFacture"},
        "ID_Fournisseur": {
            "source_file": "Ancien Factures",
            "source_col": "CodeFournisseur",
            "is_ref": True,
            "ref_model": "Fournisseurs",
            "ref_key": "Code"
        },
        "ID_Article": {
            "source_file": "Ancien Factures",
            "source_col": "CodeArticle",
            "is_ref": True,
            "ref_model": "Articles",
            "ref_key": "Reference"
        },
        "Quantite": {"source_file": "Ancien Factures", "source_col": "QuantiteCommandee"},
        "Prix_Total": {"source_file": "Ancien Factures", "source_col": "MontantTotal"}
    }
}

DEMO_DESCRIPTIONS = {
    "welcome": """
    ## Bienvenue dans l'assistant d'import Kimaiko!
    
    Cet outil vous aide à préparer vos données pour l'import dans Kimaiko en :
    - Gérant les références entre les fichiers avec des UUID
    - Mappant les colonnes automatiquement
    - Générant les fichiers au format attendu par Kimaiko
    """,
    
    "demo_mode": """
    🎮 Mode Démonstration
    
    Les fichiers et mappings sont pré-configurés pour vous montrer le fonctionnement.
    Suivez les explications à chaque étape pour comprendre le processus.
    """,
    
    "templates": """
    ### 📋 Les modèles Kimaiko
    
    En mode démo, nous avons déjà chargé 3 modèles :
    1. **Fournisseurs** : Structure pour les données fournisseurs
    2. **Articles** : Structure pour le catalogue produits
    3. **Factures** : Structure pour les factures avec références
    
    Ces modèles représentent le format attendu par Kimaiko.
    """,
    
    "source_files": """
    ### 📥 Les données sources
    
    En mode démo, nous avons 3 fichiers de l'ancien système :
    1. **Ancien Fournisseurs** : Liste des fournisseurs
    2. **Ancien Articles** : Catalogue des produits
    3. **Ancien Factures** : Historique des factures
    
    Remarquez les différences de structure avec les modèles Kimaiko.
    """,
    
    "mapping": """
    ### 🔗 Mapping et génération des fichiers
    
    En mode démo, le mapping est pré-configuré :
    
    1. **Fournisseurs** → **Ancien Fournisseurs**
       - Les noms de colonnes sont mappés automatiquement
       - Un UUID unique est généré pour chaque fournisseur
    
    2. **Articles** → **Ancien Articles**
       - Les données sont mappées vers le format Kimaiko
       - L'ID_Fournisseur est remplacé par l'UUID correspondant
    
    3. **Factures** → **Ancien Factures**
       - Les références vers les fournisseurs et articles sont mises à jour
       - Les UUID maintiennent les liens entre les fichiers
    """
}
