import json
import jsonschema
from jsonschema import validate
from typing import Dict, Any
import sys
from colorama import init, Fore, Style

# Initialiser colorama pour les couleurs dans le terminal
init()

def charger_json(chemin_fichier: str) -> Dict[str, Any]:
    """
    Charge un fichier JSON et retourne son contenu.
    """
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            return json.load(fichier)
    except FileNotFoundError:
        print(f"{Fore.RED}Erreur: Le fichier {chemin_fichier} n'existe pas.{Style.RESET_ALL}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Erreur: Le fichier {chemin_fichier} n'est pas un JSON valide: {e}{Style.RESET_ALL}")
        sys.exit(1)

def valider_schema(donnees: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """
    Valide les données par rapport au schéma.
    Retourne True si valide, False sinon.
    """
    try:
        validate(instance=donnees, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        print(f"{Fore.RED}Erreur de validation:{Style.RESET_ALL}")
        print(f"Chemin: {' -> '.join(str(x) for x in e.path)}")
        print(f"Message: {e.message}")
        return False

def main():
    print(f"{Fore.CYAN}Début de la validation du schéma...{Style.RESET_ALL}")

    # Charger le schéma propre
    print("\nChargement du schéma propre...")
    schema = charger_json('schema_clean.json')
    print(f"{Fore.GREEN}✓ Schéma chargé avec succès{Style.RESET_ALL}")

    # Charger les données
    print("\nChargement des données...")
    donnees = charger_json('exported_wizards.json')
    print(f"{Fore.GREEN}✓ Données chargées avec succès{Style.RESET_ALL}")

    # Valider les données
    print("\nValidation des données...")
    if valider_schema(donnees, schema):
        print(f"\n{Fore.GREEN}✓ Les données sont valides selon le schéma !{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}✗ Les données ne sont pas valides selon le schéma.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Fore.RED}Une erreur inattendue s'est produite: {e}{Style.RESET_ALL}")
        sys.exit(1)