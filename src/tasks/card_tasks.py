from prefect import task, context
import json
import time
import os
from src.api.card_client import CardClient

client = CardClient()

@task(log_prints=True)
def search_cards():
    cards = client.get_all_cards()
    print("Pesquisado todos os dados")
    print(json.dumps(cards[0], indent=2, ensure_ascii=False))
    return cards

@task(log_prints=True)
def search_specific_card(data):
    specific_card = data[0]
    card = client.get_card_by_id(specific_card['id'])
    
    print("Card específico:")
    print(f'Name: {card["name"]}')
    return card

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
    
    cards = client.get_cards_by_rarity('Special')
    
    if retry_count < possible_retries:
        time.sleep(5)
    
    print("Busca especial finalizada")
    return cards