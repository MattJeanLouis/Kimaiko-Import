# Import Kimaiko - Guide d'Utilisation

Ce logiciel permet d'importer et de traiter des données depuis des fichiers Excel. L'outil est flexible et peut traiter n'importe quel nombre de fichiers Excel avec leurs propres structures de données.

## Installation avec Docker

1. Assurez-vous d'avoir Docker installé sur votre ordinateur
   - Pour Windows : Téléchargez et installez Docker Desktop depuis https://www.docker.com/products/docker-desktop
   - Pour Mac : Téléchargez et installez Docker Desktop depuis https://www.docker.com/products/docker-desktop
   - Pour Linux : Suivez les instructions sur https://docs.docker.com/engine/install/

2. Construisez l'image Docker :
   ```
   docker build -t import-kimaiko .
   ```

3. Lancez le conteneur :
   ```
   docker run -p 8501:8501 import-kimaiko
   ```

4. Ouvrez votre navigateur et accédez à :
   ```
   http://localhost:8501
   ```

## Utilisation

### Mode Standard

1. Importez vos modèles Kimaiko (Étape 1) :
   - Chargez les fichiers Excel qui définissent la structure cible
   - L'interface affichera les colonnes requises pour chaque modèle

2. Importez vos données sources (Étape 2) :
   - Chargez autant de fichiers Excel que nécessaire
   - Chaque fichier peut avoir sa propre structure
   - Un aperçu des données sera affiché pour chaque fichier

3. Configurez le mapping (Étape 3) :
   - Pour chaque colonne du modèle cible :
     * Sélectionnez le fichier source
     * Choisissez la colonne correspondante
     * Indiquez si c'est une référence vers un autre modèle
   - Le système gère automatiquement la génération des identifiants uniques

4. Générez les fichiers :
   - Cliquez sur "Générer et télécharger les résultats"
   - Récupérez le fichier ZIP contenant tous les fichiers convertis

### Mode Démo

Pour vous familiariser avec l'outil :

1. Sélectionnez "Mode Démo"
2. Suivez le guide pas à pas avec des exemples pré-configurés
3. Observez comment les fichiers sont liés et convertis

## Format des Fichiers

### Fichiers Sources
- Format accepté : Excel (.xlsx)
- Pas de limite sur le nombre de fichiers
- Structure libre des colonnes
- Possibilité de définir des relations entre fichiers

### Fichiers Générés
- Fichiers Excel au format Kimaiko
- Identifiants uniques (UUID) générés automatiquement
- Relations entre fichiers préservées
- Rapport de conversion inclus

## Résultats

Le système génère :
1. Les fichiers convertis au format Kimaiko
2. Un rapport détaillé du traitement
3. Les statistiques de conversion (nombre de lignes, fichiers traités)

## Support

En cas de problème :
1. Vérifiez le format de vos fichiers Excel
2. Consultez les messages d'erreur détaillés dans l'interface
3. Assurez-vous que toutes les colonnes requises sont mappées

Les fichiers de démonstration sont fournis comme exemples mais ne limitent pas les possibilités de l'outil.
