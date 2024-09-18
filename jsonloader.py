import json

try:
    with open('Json/themes.json', 'r') as file:
        themes = json.load(file)
        print(themes)
except FileNotFoundError:
    print("Le fichier 'themes.json' n'a pas été trouvé. Veuillez vérifier son emplacement.")
    themes = {}  # Utilisez un dictionnaire vide par défaut
except json.JSONDecodeError:
    print("Le fichier 'themes.json' n'est pas un fichier JSON valide.")
    themes = {}