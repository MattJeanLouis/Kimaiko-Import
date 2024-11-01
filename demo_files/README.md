# Fichiers de Démonstration pour l'Import Kimaiko

Ce dossier contient les fichiers de test pour valider le fonctionnement de l'import Kimaiko.

## Modèles Kimaiko

1. `fournisseurs.xlsx`
   - Structure pour l'import des fournisseurs
   - Colonnes:
     * ID (UUID, généré automatiquement)
     * Nom (texte)
     * Email (texte, format email)
     * Telephone (texte)
     * Adresse (texte)

2. `articles.xlsx`
   - Structure pour l'import des articles
   - Colonnes:
     * ID (UUID, généré automatiquement)
     * Reference (texte, unique)
     * Nom (texte)
     * Prix (nombre décimal)
     * ID_Fournisseur (UUID, référence vers fournisseurs.ID)

3. `factures.xlsx`
   - Structure pour l'import des factures
   - Colonnes:
     * ID (UUID, généré automatiquement)
     * Numero (texte, unique)
     * Date (date)
     * ID_Fournisseur (UUID, référence vers fournisseurs.ID)
     * ID_Article (UUID, référence vers articles.ID)
     * Quantite (nombre entier)
     * Prix_Total (nombre décimal)

## Données Sources (Ancien Système)

1. `old_suppliers.xlsx`
   - Données des fournisseurs de l'ancien système
   - Colonnes:
     * Code (texte, clé primaire)
     * RaisonSociale (texte)
     * ContactEmail (texte)
     * NumeroTel (texte)
     * AdresseComplete (texte)

2. `old_products.xlsx`
   - Données des articles de l'ancien système
   - Colonnes:
     * CodeArticle (texte, clé primaire)
     * Designation (texte)
     * PrixUnitaire (nombre décimal)
     * CodeFournisseur (texte, clé étrangère vers Code fournisseur)

3. `old_invoices.xlsx`
   - Données des factures de l'ancien système
   - Colonnes:
     * NumeroFacture (texte, clé primaire)
     * DateFacture (date)
     * CodeFournisseur (texte, clé étrangère vers Code fournisseur)
     * CodeArticle (texte, clé étrangère vers CodeArticle)
     * QuantiteCommandee (nombre entier)
     * MontantTotal (nombre décimal)

## Configuration du Mapping

### Fournisseurs
| Colonne Kimaiko | Type         | Colonne Source  | Notes |
|----------------|--------------|-----------------|-------|
| ID             | UUID         | -               | Généré |
| Nom            | Texte        | RaisonSociale   | - |
| Email          | Texte        | ContactEmail    | - |
| Telephone      | Texte        | NumeroTel       | - |
| Adresse        | Texte        | AdresseComplete | - |

### Articles
| Colonne Kimaiko | Type         | Colonne Source  | Notes |
|----------------|--------------|-----------------|-------|
| ID             | UUID         | -               | Généré |
| Reference      | Texte        | CodeArticle     | - |
| Nom            | Texte        | Designation     | - |
| Prix           | Décimal      | PrixUnitaire    | - |
| ID_Fournisseur | UUID         | CodeFournisseur | Référence |

### Factures
| Colonne Kimaiko | Type         | Colonne Source     | Notes |
|----------------|--------------|-------------------|-------|
| ID             | UUID         | -                 | Généré |
| Numero         | Texte        | NumeroFacture     | - |
| Date           | Date         | DateFacture       | - |
| ID_Fournisseur | UUID         | CodeFournisseur   | Référence |
| ID_Article     | UUID         | CodeArticle       | Référence |
| Quantite       | Entier       | QuantiteCommandee | - |
| Prix_Total     | Décimal      | MontantTotal     | - |

## Ordre de Traitement

Pour maintenir l'intégrité des références, les fichiers doivent être traités dans cet ordre :
1. Fournisseurs (pas de dépendances)
2. Articles (dépend des Fournisseurs)
3. Factures (dépend des Fournisseurs et Articles)

## Validation des Données

Les fichiers de démonstration permettent de tester :
- La génération d'UUID
- La gestion des références entre fichiers
- La conversion des types de données
- Le maintien de l'intégrité référentielle

## Contraintes et Limitations

- Les valeurs NULL sont converties en chaînes vides
- Les dates doivent être au format Excel
- Les nombres décimaux utilisent le point comme séparateur
- Les UUID sont générés en format v4
- Les références manquantes sont remplacées par des chaînes vides
