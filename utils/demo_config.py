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

HELP_DESCRIPTIONS = {
    "welcome": """
    ## Bienvenue dans l'assistant d'import Kimaiko!
    
    Cet outil vous aide à préparer vos données pour l'import dans Kimaiko en :
    - Gérant les références entre les fichiers avec des UUID
    - Mappant les colonnes automatiquement
    - Générant les fichiers au format attendu par Kimaiko
    """,
    
    "example_files": """
    ### 📋 Exemples de Fichiers
    
    Les fichiers d'exemple fournis montrent la structure type :
    1. **Fournisseurs** : Structure pour les données fournisseurs
    2. **Articles** : Structure pour le catalogue produits
    3. **Factures** : Structure pour les factures avec références
    
    Ces exemples illustrent le format attendu par Kimaiko.
    """,
    
    "data_import": """
    ### 📥 Import de Données
    
    Pour importer vos données :
    1. Chargez vos fichiers Excel
    2. Vérifiez la structure détectée
    3. Configurez les mappings si nécessaire
    4. Validez et exportez les données
    
    L'assistant vous guidera à chaque étape.
    """,
    
    "mapping_help": """
    ### 🔗 Guide de Mapping
    
    Le mapping permet de :
    
    1. **Lier les données**
       - Faire correspondre les colonnes sources et cibles
       - Générer des UUID uniques pour chaque entrée
    
    2. **Gérer les relations**
       - Mapper les données entre fichiers
       - Maintenir les références avec des UUID
    
    3. **Valider les données**
       - Vérifier la cohérence des mappings
       - Assurer l'intégrité des relations
    """
}
