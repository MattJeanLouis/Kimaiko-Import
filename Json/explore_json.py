def analyser_niveaux(json_data, niveau=0, prefixe=""):
    """Affiche la structure hiérarchique du JSON"""
    if isinstance(json_data, list):
        print(f"{prefixe}├── Liste de {len(json_data)} éléments")
        if json_data and niveau < 10:  # Limite la profondeur à 10 niveaux
            # Analyse le premier élément comme exemple
            analyser_niveaux(json_data[0], niveau + 1, prefixe + "│   ")
    
    elif isinstance(json_data, dict):
        for cle in json_data.keys():
            valeur = json_data[cle]
            print(f"{prefixe}├── {cle}")
            if isinstance(valeur, (dict, list)) and niveau < 10:
                analyser_niveaux(valeur, niveau + 1, prefixe + "│   ")

# Exemple d'utilisation
import json

try:
    with open('exported_wizards.json', 'r', encoding='utf-8') as fichier:
        json_data = json.load(fichier)
    
    print("\n=== Structure hiérarchique du JSON ===")
    analyser_niveaux(json_data)

except FileNotFoundError:
    print("Erreur : Le fichier 'exported_wizards.json' n'a pas été trouvé.")
except json.JSONDecodeError:
    print("Erreur : Le fichier JSON n'est pas correctement formaté.")
