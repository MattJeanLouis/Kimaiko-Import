# Kimaiko - Guide d'Utilisation

Application de gestion et d'import de données avec fonctionnalités adaptatives selon la configuration API.

## Installation avec Docker

1. Assurez-vous d'avoir Docker installé sur votre ordinateur
   - Pour Windows : Téléchargez et installez Docker Desktop depuis https://www.docker.com/products/docker-desktop
   - Pour Mac : Téléchargez et installez Docker Desktop depuis https://www.docker.com/products/docker-desktop
   - Pour Linux : Suivez les instructions sur https://docs.docker.com/engine/install/

2. Construisez l'image Docker :
   ```
   docker build -t kimaiko-import .
   ```

3. Lancez le conteneur :
   ```
   docker run -p 8501:8501 kimaiko-import
   ```

4. Ouvrez votre navigateur et accédez à :
   ```
   http://localhost:8501
   ```

## Niveaux de Fonctionnalités

L'application s'adapte automatiquement selon votre configuration API :

### 🌱 Niveau Basic
- Disponible sans configuration API
- Fonctionnalités de base pour tous les modules
- Parfait pour découvrir l'application

### 🤖 Niveau OpenAI
- Activé avec une clé API OpenAI valide
- Fonctionnalités IA avancées :
  * Suggestions intelligentes
  * Auto-correction
  * Optimisation SEO
  * Validation intelligente

### ⭐ Niveau Complet
- Activé avec OpenAI et Kimaiko configurés
- Toutes les fonctionnalités disponibles :
  * Synchronisation Kimaiko
  * Import/Export avancé
  * Intégration complète

## Modules Principaux

### 🎨 Conception / Collection
- Création et configuration de collections
- Structure de données personnalisée
- Prévisualisation et validation
- Export au format JSON

### 🖥️ Front CMS
- Configuration des composants visuels
- Styles et mise en page
- Prévisualisation en temps réel
- Export des configurations

### 📥 Import / Clean Data
- Import de fichiers Excel
- Nettoyage et validation des données
- Gestion des doublons et valeurs manquantes
- Export des données traitées

## Configuration des API

### OpenAI API
1. Visitez [OpenAI API](https://platform.openai.com/signup)
2. Créez un compte ou connectez-vous
3. Accédez à la section API Keys
4. Créez une nouvelle clé API
5. Configurez la clé dans l'application

### Kimaiko API
- Nécessite les informations de connexion Kimaiko :
  * URL de l'API
  * Identifiants de connexion
- Contactez votre administrateur pour obtenir les accès

## Format des Fichiers

### Import de Données
- Format accepté : Excel (.xlsx)
- Structure flexible des colonnes
- Possibilité de traiter plusieurs fichiers
- Validation automatique des données

### Export
- Fichiers Excel nettoyés
- Configurations JSON
- Rapports de traitement détaillés
- Statistiques de conversion

## Support

Pour une utilisation optimale :
1. Commencez avec les fonctionnalités de base
2. Ajoutez la clé OpenAI pour les fonctionnalités IA
3. Configurez Kimaiko pour l'intégration complète
4. Consultez les messages d'aide dans l'interface

Les fonctionnalités sont automatiquement débloquées selon votre configuration, permettant une expérience progressive et adaptée à vos besoins.

## Dépôt GitHub

Pour contribuer au projet, suivez ces étapes :

1. Clonez le dépôt :
   ```
   git clone <URL-du-dépôt>
   ```

2. Créez une nouvelle branche `dev` :
   ```
   git checkout -b dev
   ```

3. Faites vos modifications et ajoutez-les :
   ```
   git add .
   ```

4. Faites un commit avec un message descriptif :
   ```
   git commit -m "Votre message de commit"
   ```

5. Poussez la branche `dev` sur GitHub :
   ```
   git push origin dev
