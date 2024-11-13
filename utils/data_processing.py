import uuid
from typing import Dict, List, Set, Any
import pandas as pd
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_uuid() -> str:
    """Generate a unique UUID string"""
    return str(uuid.uuid4())

def create_uuid_mapping(values) -> Dict[str, str]:
    """
    Create a mapping of values to UUIDs, handling duplicates and NA values.
    
    Args:
        values: An iterable of values to map to UUIDs
        
    Returns:
        Dict mapping unique values to UUIDs
        
    Example:
        >>> values = ['A', 'B', 'A', 'C', None]
        >>> mapping = create_uuid_mapping(values)
        >>> len(mapping) == 3  # Only unique values are mapped
        True
        >>> mapping['A'] == mapping['A']  # Same value maps to same UUID
        True
    """
    # Convert to set to get unique values, filtering out NA/None
    unique_values: Set = {value for value in values if pd.notna(value)}
    
    # Create mapping with consistent UUIDs for duplicate values
    return {value: generate_uuid() for value in unique_values}

def verify_mapping_integrity(mapping: Dict[str, str], values) -> bool:
    """
    Verify the integrity of a UUID mapping.
    
    Args:
        mapping: Dict mapping values to UUIDs
        values: Original values used to create the mapping
        
    Returns:
        bool: True if mapping is valid, False otherwise
        
    Checks:
    1. All non-NA values have a mapping
    2. Each unique value maps to a unique UUID
    3. Same value always maps to same UUID
    """
    # Get unique non-NA values
    unique_values = {value for value in values if pd.notna(value)}
    
    # Check all values have mappings
    mapped_values = set(mapping.keys())
    if unique_values != mapped_values:
        return False
    
    # Check UUID uniqueness (no two different values map to same UUID)
    if len(set(mapping.values())) != len(mapping):
        return False
    
    # Check consistency (same value always maps to same UUID)
    for value in values:
        if pd.notna(value) and value in mapping:
            uuid_val = mapping[value]
            # Verify this is the only value that maps to this UUID
            if sum(1 for v, u in mapping.items() if u == uuid_val) > 1:
                return False
    
    return True

def get_mapping_stats(mapping: Dict[str, str], values) -> Dict[str, int]:
    """
    Get statistics about a UUID mapping.
    
    Args:
        mapping: Dict mapping values to UUIDs
        values: Original values used to create the mapping
        
    Returns:
        Dict with statistics:
        - total_values: Total number of input values
        - unique_values: Number of unique values
        - mapped_values: Number of values with UUID mappings
        - na_values: Number of NA values
    """
    total_values = len(values)
    na_values = sum(1 for v in values if pd.isna(v))
    unique_values = len({v for v in values if pd.notna(v)})
    mapped_values = len(mapping)
    
    return {
        "total_values": total_values,
        "unique_values": unique_values,
        "mapped_values": mapped_values,
        "na_values": na_values
    }

def apply_mapping(data: Dict, mapping: Dict) -> Dict:
    """
    Applique les règles de mapping aux données
    
    Args:
        data: Données source à transformer
        mapping: Règles de mapping à appliquer
        
    Returns:
        Dict: Données transformées selon le mapping
        
    Raises:
        ValueError: Si data ou mapping sont None
    """
    if data is None or mapping is None:
        raise ValueError("Les paramètres data et mapping ne peuvent pas être None")
        
    processed = {}
    try:
        for field, config in mapping.items():
            if isinstance(config, dict):
                source_field = config.get('source', field)
                # Ajout de la gestion des transformations
                value = data.get(source_field)
                if 'transform' in config:
                    try:
                        value = config['transform'](value)
                    except Exception as e:
                        logger.error(f"Erreur de transformation pour le champ {field}: {str(e)}")
                processed[field] = value
            else:
                source_field = config
                processed[field] = data.get(source_field)
        return processed
    except Exception as e:
        logger.error(f"Erreur lors du mapping: {str(e)}")
        raise

def process_model(model, source_data, mappings):
    """
    Traite un modèle spécifique selon les mappings définis
    
    Args:
        model: Nom du modèle à traiter
        source_data: Données source
        mappings: Configuration des mappings
    """
    try:
        logger.info(f"\nTraitement du modèle: {model}")
        # Logique de traitement du modèle
        model_data = source_data.get(model, {})
        model_mapping = mappings.get(model, {})
        
        # Traitement des données selon le mapping
        processed_data = apply_mapping(model_data, model_mapping)
        
        # Sauvegarde ou autre traitement
        save_processed_data(model, processed_data)
        
    except Exception as e:
        logger.error(f"Erreur lors du traitement du modèle {model}: {str(e)}")
        raise ProcessingError(f"Échec du traitement pour {model}") from e

def generate_kimaiko_files(source_data, mappings, output_dir):
    """Version modifiée qui vérifie d'abord l'ordre de traitement"""
    try:
        # Analyser l'ordre de traitement
        order_analysis = suggest_processing_order(mappings)
        
        if not order_analysis['success']:
            logger.error(f"Erreur d'analyse des dépendances: {order_analysis['error']}")
            raise ValueError(order_analysis['message'])
        
        # Afficher l'ordre de traitement suggéré
        logger.info("Ordre de traitement suggéré:")
        for i, model in enumerate(order_analysis['processing_order'], 1):
            deps = order_analysis['dependencies'][model]
            logger.info(f"{i}. {model}")
            if deps['depends_on']:
                logger.info(f"   Dépend de: {', '.join(deps['depends_on'])}")
        
        # Demander confirmation à l'utilisateur
        proceed = input("Voulez-vous continuer avec cet ordre de traitement ? (o/n): ")
        if proceed.lower() != 'o':
            logger.info("Opération annulée par l'utilisateur")
            return
        
        # Procéder au traitement dans l'ordre déterminé
        for model in order_analysis['processing_order']:
            process_model(model, source_data, mappings)
            
    except Exception as e:
        logger.error(f"Erreur lors de la génération des fichiers: {str(e)}")
        raise

def suggest_processing_order(mappings: Dict) -> Dict:
    """
    Analyse les dépendances entre modèles et suggère un ordre de traitement.
    
    Args:
        mappings: Dictionnaire des configurations de mapping
        
    Returns:
        Dict contenant:
        - success: bool
        - processing_order: Liste ordonnée des modèles
        - dependencies: Dict des dépendances par modèle
        - error: Message d'erreur (si success=False)
    """
    dependencies = {}
    
    # Analyser les dépendances pour chaque modèle
    for model, config in mappings.items():
        depends_on = set()
        # Chercher les références à d'autres modèles dans le mapping
        for field_config in config.values():
            if isinstance(field_config, dict) and 'reference' in field_config:
                depends_on.add(field_config['reference']['model'])
        dependencies[model] = {'depends_on': depends_on}
    
    # Créer l'ordre de traitement (modèles sans dépendances d'abord)
    processing_order = []
    remaining = set(mappings.keys())
    
    while remaining:
        # Trouver les modèles qui n'ont plus de dépendances non traitées
        ready = {model for model in remaining 
                if not dependencies[model]['depends_on'] - set(processing_order)}
        
        if not ready:
            return {
                'success': False,
                'error': 'Dépendances circulaires détectées',
                'dependencies': dependencies
            }
        
        processing_order.extend(sorted(ready))  # Tri pour ordre consistant
        remaining -= ready
    
    return {
        'success': True,
        'processing_order': processing_order,
        'dependencies': dependencies
    }

class ProcessingError(Exception):
    """Exception personnalisée pour les erreurs de traitement"""
    pass

def save_processed_data(model: str, data: Dict, output_dir: str = "output", format: str = "both") -> None:
    """
    Sauvegarde les données traitées en JSON et/ou Excel
    
    Args:
        model: Nom du modèle
        data: Données à sauvegarder
        output_dir: Répertoire de sortie
        format: Format de sortie ('json', 'excel', ou 'both')
    """
    # Créer le répertoire de sortie avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_dir, model, timestamp)
    os.makedirs(output_path, exist_ok=True)
    
    try:
        if format.lower() in ['json', 'both']:
            # Sauvegarde JSON
            json_path = os.path.join(output_path, f"{model}.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Données JSON sauvegardées dans {json_path}")
            
        if format.lower() in ['excel', 'both']:
            # Sauvegarde Excel
            excel_path = os.path.join(output_path, f"{model}.xlsx")
            # Conversion en DataFrame (ajustez selon votre structure de données)
            if isinstance(data, dict):
                df = pd.DataFrame([data])
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            else:
                df = pd.DataFrame(data)
            
            df.to_excel(excel_path, index=False)
            logger.info(f"Données Excel sauvegardées dans {excel_path}")
            
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde de {model}: {str(e)}")
        raise

def validate_mapping_config(mappings: Dict) -> bool:
    """
    Valide la configuration des mappings
    
    Args:
        mappings: Configuration des mappings à valider
        
    Returns:
        bool: True si la configuration est valide
        
    Raises:
        ValueError: Si la configuration est invalide
    """
    try:
        for model, config in mappings.items():
            if not isinstance(config, dict):
                raise ValueError(f"Configuration invalide pour le modèle {model}")
            
            for field, field_config in config.items():
                if isinstance(field_config, dict):
                    required_keys = {'source'}
                    if not required_keys.issubset(field_config.keys()):
                        raise ValueError(f"Configuration incomplète pour {model}.{field}")
        return True
    except Exception as e:
        logger.error(f"Configuration invalide: {str(e)}")
        return False

def backup_data(data: Dict, model: str, backup_dir: str = "backups") -> None:
    """
    Crée une sauvegarde des données avant traitement
    
    Args:
        data: Données à sauvegarder
        model: Nom du modèle
        backup_dir: Répertoire de sauvegarde
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, model, timestamp)
    os.makedirs(backup_path, exist_ok=True)
    
    backup_file = os.path.join(backup_path, f"{model}_backup.json")
    with open(backup_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Backup créé dans {backup_file}")

def validate_data_structure(data: Dict, expected_fields: Set[str]) -> bool:
    """
    Vérifie que les données contiennent les champs requis
    
    Args:
        data: Données à valider
        expected_fields: Ensemble des champs attendus
        
    Returns:
        bool: True si la structure est valide
    """
    missing_fields = expected_fields - set(data.keys())
    if missing_fields:
        logger.error(f"Champs manquants: {missing_fields}")
        return False
    return True
