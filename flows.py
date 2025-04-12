from prefect import flow, task, context
from dotenv import load_dotenv
import os
import requests
import json
import time

load_dotenv()

@task(log_prints=True)
def search_cards() -> str:
    url = os.environ.get("URL_API")
    response = requests.get(f'{url}/cards')
    all_cards = response.json()
    cards = all_cards['cards'] 
    first_card = cards[0]

    print("Pesquisado todos os dados")
    print(json.dumps(first_card, indent=2, ensure_ascii=False))

    return cards

@task(log_prints=True)
def search_specific_card(data):
    url = os.environ.get("URL_API")
    specific_card = data[0]
    response = requests.get(f'{url}/cards/{specific_card['id']}')
    card = (response.json())['card']
    
    print("Card específico:")
    print(f'Name: {card['name']}')

@task(
    log_prints=True,
    retries=3,
    timeout_seconds=4,
    retry_delay_seconds=2
)
def search_special_rarity():
    run_context = context.get_run_context()
    retry_count = run_context.task_run.run_count
    possible_retries = int(os.environ.get("QT_RETRY"))
    
    print(f"Tentativa número: {retry_count}")
    
    rarity = 'Special'
    response = requests.get(f'https://api.magicthegathering.io/v1/cards?rarity={rarity}')
    all_cards = response.json()
    cards = all_cards['cards']
    
    if retry_count < possible_retries:
        time.sleep(5)
    
    print("Busca especial finalizada")
    return cards

@flow(log_prints=True)
def project():
    data = search_cards()
    search_specific_card(data)
    data_special = search_special_rarity()
    search_specific_card(data_special)

project()