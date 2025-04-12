from prefect import flow, task
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

@task(log_prints=True)
def search_cards() -> str:
    url = os.environ.get("URL_API")
    response = requests.get(f'{url}/cards')
    all_cards = response.json()
    cards = all_cards['cards'] 

    print("Pesquisado todos os dados")
    print(cards[0])
    return cards

@task(log_prints=True)
def search_specific_card(data):
    url = os.environ.get("URL_API")
    specific_card = data[0]
    response = requests.get(f'{url}/cards/{specific_card['id']}')
    card = (response.json())['card']
    print("Card específico:")
    print(json.dumps(card, indent=2, ensure_ascii=False))

@flow(log_prints=True)
def project():
    data = search_cards()
    search_specific_card(data)

project()