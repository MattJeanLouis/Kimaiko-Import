import pandas as pd
import os
from pathlib import Path

# Get the current script's directory
SCRIPT_DIR = Path(__file__).parent.absolute()

# 1. Création des modèles Kimaiko (templates)

# Fournisseurs template
fournisseurs_template = pd.DataFrame({
    'ID': ['UUID-1'],
    'Nom': ['Example Corp'],
    'Email': ['contact@example.com'],
    'Telephone': ['+33123456789'],
    'Adresse': ['123 Rue Example, 75001 Paris']
})
fournisseurs_template.to_excel(SCRIPT_DIR / 'fournisseurs.xlsx', index=False)

# Articles template
articles_template = pd.DataFrame({
    'ID': ['UUID-1'],
    'Reference': ['ART001'],
    'Nom': ['Produit Example'],
    'Prix': [99.99],
    'ID_Fournisseur': ['UUID-F1']
})
articles_template.to_excel(SCRIPT_DIR / 'articles.xlsx', index=False)

# Factures template
factures_template = pd.DataFrame({
    'ID': ['UUID-1'],
    'Numero': ['FAC001'],
    'Date': ['2024-01-01'],
    'ID_Fournisseur': ['UUID-F1'],
    'ID_Article': ['UUID-A1'],
    'Quantite': [5],
    'Prix_Total': [499.95]
})
factures_template.to_excel(SCRIPT_DIR / 'factures.xlsx', index=False)

# 2. Création des données sources (ancien système)

# Fournisseurs source
old_suppliers = pd.DataFrame({
    'Code': ['SUP001', 'SUP002', 'SUP003'],
    'RaisonSociale': ['Tech Solutions', 'Digital Services', 'Green IT'],
    'ContactEmail': ['info@techsolutions.com', 'contact@digitalservices.fr', 'support@greenit.fr'],
    'NumeroTel': ['+33612345678', '+33698765432', '+33634567890'],
    'AdresseComplete': [
        '45 Avenue Innovation, 69002 Lyon',
        '88 Rue Numérique, 33000 Bordeaux',
        '12 Boulevard Écologie, 44000 Nantes'
    ]
})
old_suppliers.to_excel(SCRIPT_DIR / 'old_suppliers.xlsx', index=False)

# Articles source
old_products = pd.DataFrame({
    'CodeArticle': ['PROD001', 'PROD002', 'PROD003', 'PROD004', 'PROD005'],
    'Designation': [
        'Ordinateur Portable Pro',
        'Écran 27" 4K',
        'Clavier Mécanique',
        'Souris Ergonomique',
        'Station d\'Accueil'
    ],
    'PrixUnitaire': [1299.99, 499.99, 129.99, 79.99, 199.99],
    'CodeFournisseur': ['SUP001', 'SUP001', 'SUP002', 'SUP002', 'SUP003']
})
old_products.to_excel(SCRIPT_DIR / 'old_products.xlsx', index=False)

# Factures source
old_invoices = pd.DataFrame({
    'NumeroFacture': ['INV2024-001', 'INV2024-002', 'INV2024-003', 'INV2024-004', 'INV2024-005'],
    'DateFacture': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
    'CodeFournisseur': ['SUP001', 'SUP001', 'SUP002', 'SUP002', 'SUP003'],
    'CodeArticle': ['PROD001', 'PROD002', 'PROD003', 'PROD004', 'PROD005'],
    'QuantiteCommandee': [2, 3, 5, 4, 2],
    'MontantTotal': [2599.98, 1499.97, 649.95, 319.96, 399.98]
})
old_invoices.to_excel(SCRIPT_DIR / 'old_invoices.xlsx', index=False)

# 3. Création du README
readme_content = """# Fichiers de Démonstration pour l'Import Kimaiko

Ce dossier contient des fichiers Excel de démonstration pour tester l'application d'import Kimaiko.

## Modèles Kimaiko

1. `fournisseurs.xlsx`
   - Structure pour l'import des fournisseurs
   - Colonnes: ID, Nom, Email, Telephone, Adresse

2. `articles.xlsx`
   - Structure pour l'import des articles
   - Colonnes: ID, Reference, Nom, Prix, ID_Fournisseur

3. `factures.xlsx`
   - Structure pour l'import des factures
   - Colonnes: ID, Numero, Date, ID_Fournisseur, ID_Article, Quantite, Prix_Total

## Données Sources (Ancien Système)

1. `old_suppliers.xlsx`
   - Données des fournisseurs de l'ancien système
   - Colonnes: Code, RaisonSociale, ContactEmail, NumeroTel, AdresseComplete

2. `old_products.xlsx`
   - Données des articles de l'ancien système
   - Colonnes: CodeArticle, Designation, PrixUnitaire, CodeFournisseur

3. `old_invoices.xlsx`
   - Données des factures de l'ancien système
   - Colonnes: NumeroFacture, DateFacture, CodeFournisseur, CodeArticle, QuantiteCommandee, MontantTotal

## Utilisation

1. Commencez par importer les modèles Kimaiko (`fournisseurs.xlsx`, `articles.xlsx`, `factures.xlsx`)
2. Importez ensuite les données sources (`old_suppliers.xlsx`, `old_products.xlsx`, `old_invoices.xlsx`)
3. Effectuez le mapping en suivant ces correspondances:

### Mapping Fournisseurs
- ID → Généré automatiquement (UUID)
- Nom → RaisonSociale
- Email → ContactEmail
- Telephone → NumeroTel
- Adresse → AdresseComplete

### Mapping Articles
- ID → Généré automatiquement (UUID)
- Reference → CodeArticle
- Nom → Designation
- Prix → PrixUnitaire
- ID_Fournisseur → CodeFournisseur (avec UUID)

### Mapping Factures
- ID → Généré automatiquement (UUID)
- Numero → NumeroFacture
- Date → DateFacture
- ID_Fournisseur → CodeFournisseur (avec UUID)
- ID_Article → CodeArticle (avec UUID)
- Quantite → QuantiteCommandee
- Prix_Total → MontantTotal

Les UUID seront générés automatiquement pour maintenir les références entre les fichiers."""

with open(SCRIPT_DIR / 'README.md', 'w', encoding='utf-8') as f:
    f.write(readme_content)

print("✅ Fichiers de démonstration générés avec succès!")
print("📁 Vérifiez le dossier 'demo_files' pour les fichiers suivants:")
print("   - Modèles Kimaiko: fournisseurs.xlsx, articles.xlsx, factures.xlsx")
print("   - Données sources: old_suppliers.xlsx, old_products.xlsx, old_invoices.xlsx")
print("   - Documentation: README.md")
