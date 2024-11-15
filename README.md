# Application de Conception de Collections

Cette application est un outil basé sur Streamlit conçu pour aider à concevoir des collections pour un système de gestion. Elle guide les utilisateurs à travers plusieurs phases, y compris la collecte d'informations sur l'entreprise, la génération de collections, le détail de ces collections, et la génération de documentation.

## Fonctionnalités

- **Collecte d'Informations** : Rassemblez des informations détaillées sur l'entreprise, y compris la mission, les produits, le marché cible, et plus encore.
- **Génération de Collections** : Utilise l'IA pour générer et affiner automatiquement des collections adaptées aux besoins de l'entreprise.
- **Attributs Détaillés des Collections** : Définissez des attributs détaillés pour chaque collection, y compris les types de données et les contraintes.
- **Génération de Documentation** : Créez une documentation complète pour les collections et leurs relations.

## Logique et Fonctionnement

L'application est divisée en plusieurs phases :

1. **Phase de Collecte d'Informations** : L'utilisateur entre des informations clés sur l'entreprise. Ces données sont utilisées pour personnaliser les collections générées.

2. **Phase de Génération de Collections** : L'application utilise l'API OpenAI pour analyser les informations fournies et proposer une liste initiale de collections. Elle peut également suggérer des collections supplémentaires pour compléter le système.

3. **Phase de Détail des Collections** : Pour chaque collection, l'application génère une structure détaillée des attributs, incluant le type de données, les contraintes, et les relations potentielles avec d'autres collections.

4. **Phase de Documentation** : L'application compile toutes les informations et génère une documentation technique complète au format Markdown, incluant une vue d'ensemble du système, l'architecture des données, et les recommandations d'implémentation.

## Installation

### Prérequis

- Python 3.9 ou plus récent
- Docker (optionnel, pour un déploiement containerisé)

### Configuration Locale

1. **Clonez le dépôt** :
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Créez un environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows utilisez `venv\Scripts\activate`
   ```

3. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Exécutez l'application** :
   ```bash
   streamlit run app.py
   ```

### Configuration Docker

1. **Construisez l'image Docker** :
   ```bash
   docker build -t kimaiko-import-alpha .
   ```

2. **Exécutez le conteneur Docker** :
   ```bash
   docker run -p 8501:8501 kimaiko-import-alpha
   ```

## Utilisation

- Accédez à l'application dans votre navigateur web à l'adresse `http://localhost:8501`.
- Suivez les instructions à l'écran pour entrer les informations de l'entreprise et générer des collections.
- Utilisez la documentation générée pour une implémentation et une intégration ultérieures.

## Dépendances

- **Streamlit** : Pour construire l'interface web.
- **OpenAI** : Pour l'analyse et la génération pilotées par l'IA.
- **Pandas** : Pour la manipulation des données.
- **Tabulate** : Pour la présentation des données.

## Structure et Documentation

### Format JSON de Sortie

L'application génère une documentation technique basée sur un format JSON spécifique qui comprend :

1. **Collections** (Tables de données)
   - UUID et métadonnées
   - Champs et propriétés
   - Relations et contraintes

2. **Pages** (Interface utilisateur)
   - Configuration d'affichage
   - Composants et mise en page
   - Styles et comportements

3. **Rôles et Permissions**
   - Droits CRUD par collection
   - Visibilité des champs
   - Associations avec les pages

### Fichiers de Référence

Le dossier `json/` contient des exemples et modèles qui illustrent la structure attendue :

- `exported_wizards.json` : Modèle complet de configuration
- Autres fichiers JSON : Exemples spécifiques pour chaque composant

### Génération de Documentation

La phase finale de l'application (`phase5_generation_documentation`) :
1. Analyse toutes les données collectées
2. Les structure selon le format JSON requis
3. Génère une documentation technique complète incluant :
   - Vue d'ensemble du système
   - Architecture des données
   - Description des collections
   - Relations et dépendances
   - Contraintes et règles métier
   - Recommandations d'implémentation

### Validation et Export

La documentation générée peut être :
- Visualisée directement dans l'interface
- Téléchargée au format Markdown
- Utilisée comme référence pour l'implémentation