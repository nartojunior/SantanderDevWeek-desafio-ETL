import pandas as pd # On Terminal: pip install pandas[excel]
import requests as req # On Terminal: pip install requests
import json
import openai # On Terminal: pip install --upgrade openai
import os

sdw_2023_api = "https://sdw-2023-prd.up.railway.app"

df = pd.read_csv("SDW2003.csv")

user_ids = df['UserId'].tolist()

print (user_ids)

def get_user(id):
    response = req.get(f"{sdw_2023_api}/users/{id}")
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id))  is not None]

print (json.dumps(users, indent=2))

openai_api_key = os.getenv("OPENAI_KEY")

openai.api_key = openai_api_key

def generate_ai_news(user):

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um game designer."},
            {"role": "user", "content": f"Crie uma mensagem para {user['name']} com a tendência de game design para jogos indie. (máximo de 100 caracteres)"}          
        ]
        
    )

    return response['choices'][0]['message']['content'].strip('\"')

# Substituto da resposta da api (feito à mão no chat da OpenAI)
news = [
        "SDW, mergulhe na magia dos jogos indie, onde a criatividade é a protagonista! Explore novos mundos e histórias únicas.",
        "Explore a magia dos jogos indie: mergulhe em narrativas envolventes, mecânicas inovadoras e arte única. Crie sua própria jornada. #IndieGaming 🎮✨",
        "SDW, mergulhe na criatividade indie: mecânicas únicas, narrativas envolventes e visuais cativantes aguardam sua jornada! 🎮🌟 #IndieGameDesign"]

for indice, user in enumerate(users):
    #news = generate_ai_news(user) # Sem $$$ para testar.
    print (news)
    user['news'].append({
        "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
        "description": news[indice]
    })

def update_user(user):
    response = req.put(f"{sdw_2023_api}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for user in users:
    success = update_user(user)
    print (f"User {user['name']} updated? {success}")