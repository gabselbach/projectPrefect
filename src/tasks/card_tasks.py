import json
import os
import time

from prefect.logging import get_run_logger
from src.api.card_client import CardClient
from prefect import task, context

client = CardClient()

@task(log_prints=True)
def search_cards():
    logger = get_run_logger()
    cards = client.get_all_cards()
    logger.info("Pesquisado todos os dados")
    logger.info(json.dumps(cards[0], indent=2, ensure_ascii=False))
    return cards

@task(log_prints=True)
def search_specific_card(data):
    logger = get_run_logger()
    specific_card = data[0]
    card = client.get_card_by_id(specific_card['id'])
    
    logger.info("Card específico:")
    logger.info(f'Name: {card["name"]}')
    return card

@task(
    log_prints=True,
    retries=3,
    timeout_seconds=4,
    retry_delay_seconds=2
)
def search_special_rarity():
    logger = get_run_logger()
    run_context = context.get_run_context()
    retry_count = run_context.task_run.run_count
    possible_retries = int(os.environ.get("QT_RETRY"))
    
    logger.info(f"Tentativa número: {retry_count}")
    
    cards = client.get_cards_by_rarity('Special')
    
    if retry_count < possible_retries:
        time.sleep(5)
    
    logger.info("Busca especial finalizada")
    return cards