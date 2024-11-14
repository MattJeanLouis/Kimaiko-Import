import os
from openai import OpenAI

def faire_requete_chatgpt(prompt):
    # Initialiser le client OpenAI avec la clé API
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        # Faire la requête à l'API ChatGPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        
        # Retourner la réponse générée
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Erreur lors de la requête à ChatGPT: {str(e)}")
        return None

# Exemple d'utilisation dans une fonction
def test_faire_requete_chatgpt():
    prompt = "Qui est le président de la France ?"
    print(faire_requete_chatgpt(prompt))

#test_faire_requete_chatgpt()