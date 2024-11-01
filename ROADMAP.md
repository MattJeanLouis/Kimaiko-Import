# Roadmap - Import Kimaiko v2

## 1. Amélioration de l'Interface Utilisateur
- [ ] Refonte complète de l'interface pour plus de clarté
- [ ] Prévisualisation en temps réel des mappings
- [ ] Interface drag & drop améliorée
- [ ] Thème moderne et responsive

## 2. Système de Mapping Réutilisable
- [ ] Sauvegarde des configurations de mapping dans des fichiers JSON
- [ ] Export automatique des configurations dans le dossier résultat
- [ ] Interface de gestion des configurations sauvegardées
- [ ] Import/Export des configurations de mapping
- [ ] Système de templates de mapping

## 3. Support Multi-Format
- [ ] Support des fichiers JSON en entrée
- [ ] Support CSV avec détection automatique du délimiteur
- [ ] Support XML
- [ ] API REST pour l'import de données
- [ ] Possibilité d'exporter vers différents formats

## 4. Mapping Intelligent avec IA
- [ ] Intégration de l'API OpenAI
- [ ] Suggestion automatique de mapping basée sur le contenu
- [ ] Détection intelligente des relations entre fichiers
- [ ] Assistant IA pour la configuration
- [ ] Validation intelligente des données

## Spécifications Techniques

### Configuration IA
- Utilisation de l'API OpenAI GPT-4
- Modèles de prompt pour l'analyse des données
- Cache local pour optimiser les appels API

### Format des Fichiers de Configuration
```json
{
  "mapping_name": "config_name",
  "source_type": "excel|json|csv|xml",
  "mappings": {
    "target_field": {
      "source_file": "file_name",
      "source_field": "field_name",
      "transformations": []
    }
  },
  "ai_suggestions": {
    "enabled": true,
    "confidence_threshold": 0.8
  }
}
```

### Compatibilité
- Rétrocompatibilité avec les fichiers de la v1
- Migration automatique des anciens mappings
- Support des anciennes configurations
