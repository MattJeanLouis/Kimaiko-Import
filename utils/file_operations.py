import pandas as pd
from pathlib import Path
import zipfile
import tempfile
import os
from typing import Dict, Optional
import gc
import logging
import traceback
from .data_processing import generate_uuid, create_uuid_mapping, verify_mapping_integrity, get_mapping_stats

def load_demo_files(demo_dir: Path) -> tuple[Dict, Dict]:
    """Load demonstration files and return templates and source files"""
    kimaiko_templates = {}
    source_files = {}
    
    try:
        # Load Kimaiko templates
        kimaiko_files = {
            "Fournisseurs": "fournisseurs.xlsx",
            "Articles": "articles.xlsx",
            "Factures": "factures.xlsx"
        }
        
        for name, filename in kimaiko_files.items():
            df = None
            try:
                df = pd.read_excel(demo_dir / filename)
                kimaiko_templates[name] = df.columns.tolist()
            finally:
                del df  # Free memory even if error occurs
                gc.collect()
        
        # Load source files
        source_files_map = {
            "Ancien Fournisseurs": "old_suppliers.xlsx",
            "Ancien Articles": "old_products.xlsx",
            "Ancien Factures": "old_invoices.xlsx"
        }
        
        for name, filename in source_files_map.items():
            df = None
            try:
                df = pd.read_excel(demo_dir / filename)
                source_files[name] = {
                    'columns': df.columns.tolist(),
                    'data': df
                }
            finally:
                if df is not None:
                    del df
                gc.collect()
        
        return kimaiko_templates, source_files
    except Exception as e:
        raise Exception(f"Erreur lors du chargement des fichiers: {str(e)}")
    finally:
        gc.collect()

def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Optimize DataFrame memory usage"""
    try:
        for col in df.columns:
            if df[col].dtype == 'object':
                # Convert string columns to categorical if they have few unique values
                if df[col].nunique() / len(df) < 0.5:  # Less than 50% unique values
                    df[col] = df[col].astype('category')
            elif df[col].dtype == 'float64':
                # Downcast float columns where possible
                df[col] = pd.to_numeric(df[col], downcast='float')
            elif df[col].dtype == 'int64':
                # Downcast integer columns where possible
                df[col] = pd.to_numeric(df[col], downcast='integer')
        return df
    except Exception as e:
        raise Exception(f"Erreur lors de l'optimisation du DataFrame: {str(e)}")

def process_model_data(model_name: str, model_mappings: Dict, source_files: Dict) -> tuple[pd.DataFrame, Dict[str, str], Dict[str, int]]:
    """Process data for a single model, with proper memory management"""
    source_df = None
    final_df = None
    try:
        # Find the first mapping with a source file
        source_mapping = next((m for m in model_mappings.values() 
                            if isinstance(m, dict) and "source_file" in m), None)
        if not source_mapping:
            logging.error(f"Aucun mapping source trouvé pour le modèle {model_name}")
            logging.error(f"Mappings disponibles: {model_mappings}")
            return None, None, None
        
        logging.info(f"Traitement du modèle {model_name}")
        logging.info(f"Fichier source: {source_mapping['source_file']}")
        
        if source_mapping["source_file"] not in source_files:
            logging.error(f"Fichier source '{source_mapping['source_file']}' non trouvé")
            logging.error(f"Fichiers sources disponibles: {list(source_files.keys())}")
            raise ValueError(f"Fichier source '{source_mapping['source_file']}' non trouvé")
        
        source_df = source_files[source_mapping["source_file"]]["data"].copy()
        source_df = optimize_dataframe(source_df)
        
        logging.info(f"Colonnes source disponibles: {source_df.columns.tolist()}")
        
        # Create DataFrame with UUIDs
        final_df = pd.DataFrame(index=range(len(source_df)))
        final_df["ID"] = [generate_uuid() for _ in range(len(source_df))]
        
        # Create and verify UUID mapping
        key_col = source_mapping["source_col"]
        if key_col not in source_df.columns:
            logging.error(f"Colonne source '{key_col}' non trouvée dans {source_mapping['source_file']}")
            logging.error(f"Colonnes disponibles: {source_df.columns.tolist()}")
            raise ValueError(f"Colonne source '{key_col}' non trouvée")
            
        values = source_df[key_col].values
        uuid_map = create_uuid_mapping(values)
        
        # Verify mapping integrity
        if not verify_mapping_integrity(uuid_map, values):
            logging.error(f"Échec de la vérification d'intégrité du mapping UUID pour {model_name}")
            logging.error(f"Valeurs uniques: {len(set(values))}")
            logging.error(f"UUIDs uniques: {len(set(uuid_map.values()))}")
            raise ValueError(f"Échec de la vérification d'intégrité du mapping UUID pour {model_name}")
        
        # Get mapping statistics
        mapping_stats = get_mapping_stats(uuid_map, values)
        logging.info(f"Statistiques de mapping pour {model_name}: {mapping_stats}")
        
        return final_df, uuid_map, mapping_stats
    except Exception as e:
        logging.error(f"Erreur lors du traitement du modèle {model_name}")
        logging.error(f"Message d'erreur: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise
    finally:
        if source_df is not None:
            del source_df
        gc.collect()

def map_multi_references(value: str, uuid_map: Dict[str, str]) -> str:
    """
    Map multiple references separated by commas to their corresponding UUIDs.
    
    Args:
        value: String containing one or more references separated by ", "
        uuid_map: Dictionary mapping original values to UUIDs
        
    Returns:
        String of mapped UUIDs separated by ", " or empty string if no valid mappings
    """
    if pd.isna(value):
        return ''
    
    # Split the string by ", " and strip whitespace
    refs = [ref.strip() for ref in str(value).split(", ")]
    
    # Map each reference to its UUID if it exists in the mapping
    mapped_refs = [uuid_map.get(ref, '') for ref in refs]
    
    # Filter out empty strings and join with ", "
    valid_refs = [ref for ref in mapped_refs if ref]
    return ", ".join(valid_refs) if valid_refs else ''

def process_model_references(final_df: pd.DataFrame, model_mappings: Dict, source_files: Dict, uuid_mappings: Dict) -> None:
    """Process references for a single model, with proper memory management"""
    source_df = None
    try:
        for col, mapping in model_mappings.items():
            if col == "ID" or not isinstance(mapping, dict) or "source_file" not in mapping:
                continue
            
            logging.info(f"Traitement de la colonne {col}")
            logging.info(f"Mapping: {mapping}")
            
            if mapping["source_file"] not in source_files:
                logging.error(f"Fichier source '{mapping['source_file']}' non trouvé")
                logging.error(f"Fichiers sources disponibles: {list(source_files.keys())}")
                raise ValueError(f"Fichier source '{mapping['source_file']}' non trouvé")
                
            source_df = source_files[mapping["source_file"]]["data"].copy()
            source_df = optimize_dataframe(source_df)
            
            if mapping["source_col"] not in source_df.columns:
                logging.error(f"Colonne source '{mapping['source_col']}' non trouvée dans {mapping['source_file']}")
                logging.error(f"Colonnes disponibles: {source_df.columns.tolist()}")
                raise ValueError(f"Colonne source '{mapping['source_col']}' non trouvée")
            
            if mapping.get("is_ref"):
                ref_model = mapping["ref_model"]
                if ref_model not in uuid_mappings:
                    logging.error(f"Mapping UUID non trouvé pour le modèle référencé {ref_model}")
                    logging.error(f"Mappings UUID disponibles: {list(uuid_mappings.keys())}")
                    raise ValueError(f"Mapping UUID non trouvé pour le modèle référencé {ref_model}")
                    
                source_values = source_df[mapping["source_col"]]
                # Use map_multi_references for handling multiple references in a single cell
                final_df[col] = source_values.apply(lambda x: map_multi_references(x, uuid_mappings[ref_model]))
                
                # Log reference mapping statistics
                total_refs = len(source_values)
                mapped_refs = sum(final_df[col] != '')
                logging.info(f"Statistiques de référence pour {col}:")
                logging.info(f"Total références: {total_refs}")
                logging.info(f"Références mappées: {mapped_refs}")
                logging.info(f"Références non mappées: {total_refs - mapped_refs}")
            else:
                final_df[col] = source_df[mapping["source_col"]]
            
            del source_df
            source_df = None
            gc.collect()
    except Exception as e:
        logging.error(f"Erreur lors du traitement des références")
        logging.error(f"Message d'erreur: {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise
    finally:
        if source_df is not None:
            del source_df
        gc.collect()

def generate_kimaiko_files(mappings: Dict, source_files: Dict) -> bytes:
    """Generate Kimaiko format files with UUID handling and package them in a zip"""
    temp_dir = None
    try:
        logging.info("Début de la génération des fichiers Kimaiko")
        logging.info(f"Modèles à traiter: {list(mappings.keys())}")
        logging.info(f"Fichiers sources disponibles: {list(source_files.keys())}")
        
        temp_dir = tempfile.mkdtemp()
        result_dir = Path(temp_dir) / "import_kimaiko"
        os.makedirs(result_dir)
        os.makedirs(result_dir / "fichiers_kimaiko")
        os.makedirs(result_dir / "references")
        
        # Store generated UUIDs and mapping statistics
        uuid_mappings = {}
        mapping_stats = {}
        
        # First pass: generate UUIDs for each model
        for model_name in mappings.keys():
            logging.info(f"\nTraitement du modèle: {model_name}")
            final_df = None
            try:
                final_df, uuid_map, stats = process_model_data(
                    model_name, 
                    mappings[model_name], 
                    source_files
                )
                
                if final_df is not None:
                    uuid_mappings[model_name] = uuid_map
                    mapping_stats[model_name] = stats
                    
                    logging.info(f"Traitement des références pour {model_name}")
                    # Process references
                    process_model_references(
                        final_df, 
                        mappings[model_name], 
                        source_files, 
                        uuid_mappings
                    )
                    
                    # Save optimized DataFrame
                    final_df = optimize_dataframe(final_df)
                    output_path = result_dir / "fichiers_kimaiko" / f"{model_name}.xlsx"
                    logging.info(f"Sauvegarde du fichier: {output_path}")
                    final_df.to_excel(
                        output_path,
                        index=False,
                        engine='openpyxl'
                    )
                    logging.info(f"Fichier sauvegardé avec succès: {model_name}.xlsx")
            except Exception as e:
                logging.error(f"Erreur lors du traitement du modèle {model_name}")
                logging.error(f"Message d'erreur: {str(e)}")
                logging.error(f"Traceback: {traceback.format_exc()}")
                raise Exception(f"'{model_name}': {str(e)}")
            finally:
                if final_df is not None:
                    del final_df
                gc.collect()
        
        # Create UUID mapping file with statistics
        mapping_df = None
        try:
            mapping_dfs = []
            for model_name, mapping in uuid_mappings.items():
                df = pd.DataFrame(list(mapping.items()), columns=['Valeur Originale', 'UUID'])
                df['Modèle'] = model_name
                
                # Add statistics
                stats = mapping_stats[model_name]
                df_stats = pd.DataFrame([{
                    'Valeur Originale': f"Statistiques {model_name}",
                    'UUID': f"Total: {stats['total_values']}, Uniques: {stats['unique_values']}, "
                           f"Mappés: {stats['mapped_values']}, NA: {stats['na_values']}"
                }])
                
                mapping_dfs.append(df)
                mapping_dfs.append(df_stats)
            
            if mapping_dfs:
                mapping_df = pd.concat(mapping_dfs, ignore_index=True)
                mapping_df = optimize_dataframe(mapping_df)
                mapping_df.to_excel(
                    result_dir / "references" / "references_uuid.xlsx",
                    index=False,
                    engine='openpyxl'
                )
        except Exception as e:
            logging.error("Erreur lors de la création du fichier de mapping UUID")
            logging.error(f"Message d'erreur: {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            raise
        finally:
            if mapping_df is not None:
                del mapping_df
            gc.collect()
        
        # Create README
        readme_content = """# Import Kimaiko - Fichiers Générés

## Structure des dossiers

### 📁 fichiers_kimaiko/
Contient les fichiers prêts à être importés dans Kimaiko.

### 📁 references/
- references_uuid.xlsx : Table de correspondance entre les valeurs originales et les UUID générés
  - Inclut des statistiques sur les mappings pour chaque modèle
  - Montre le nombre total de valeurs, uniques, mappées et NA

## Comment utiliser ces fichiers

1. Les fichiers dans le dossier `fichiers_kimaiko` sont prêts à être importés dans Kimaiko
2. Le fichier `references_uuid.xlsx` vous permet de retrouver les correspondances entre les anciennes et nouvelles références
3. Importez les fichiers dans l'ordre de leurs dépendances (d'abord les fichiers référencés, puis les fichiers qui les référencent)

## Notes importantes

- Les références multiples dans une cellule (séparées par ", ") sont correctement gérées
- Les références manquantes sont remplacées par des valeurs vides
- Les fichiers ont été optimisés pour gérer de grands volumes de données
- Les statistiques de mapping sont incluses dans references_uuid.xlsx"""
        
        with open(result_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        # Create ZIP file
        zip_path = Path(temp_dir) / "import_kimaiko.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(result_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(result_dir)
                    zipf.write(file_path, arc_name)
        
        logging.info("Génération des fichiers terminée avec succès")
        
        # Read ZIP content for download
        with open(zip_path, 'rb') as f:
            return f.read()
    
    except Exception as e:
        error_msg = f"Erreur lors de la génération des fichiers: {str(e)}"
        logging.error(error_msg)
        logging.error(f"Traceback: {traceback.format_exc()}")
        raise Exception(error_msg)
    finally:
        # Clean up temporary directory
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)
        gc.collect()
