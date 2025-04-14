"""Este módulo fornece tarefas para buscar informações 
sobre cards de uma API externa 

Ele define tarefas para pesquisar todos os cards, 
um card específico por ID e cards com uma raridade específica, 
implementando retentativas e timeouts quando necessário.
"""
import os
import json
import time
from prefect import task
from prefect import context

from src.api.card_client import CardClient

client = CardClient()

@task(log_prints=True)
def search_cards() -> list:
    """Pesquisa todos os cards disponíveis através de uma API Externa.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um card.
    """
    cards = client.get_all_cards()
    print("Pesquisado todos os dados")
    print(json.dumps(cards[0], indent=2, ensure_ascii=False))
    return cards

@task(log_prints=True)
def search_specific_card(data: list) -> dict:
    """Pesquisa um card específico pelo ID, utilizando os dados fornecidos.

    Args:
        data (list): Uma lista contendo um dicionário com o ID do card a ser pesquisado.
                     Espera-se que a lista contenha pelo menos um elemento com a chave 'id'.

    Returns:
        dict: Um dicionário representando o card encontrado com o ID especificado.
    """
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
def search_special_rarity() -> list:
    """Pesquisa cards com raridade 'Special' com retentativas e timeout.

    Esta tarefa tenta buscar cards com raridade 'Special' 
    e implementa lógica de retentativa em caso de falha.  
    Ela também possui um timeout para simular falhas.

    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa um card 
        com raridade 'Special'.
    """
    run_context = context.get_run_context()
    retry_count = run_context.task_run.run_count
    possible_retries = int(os.environ.get("QT_RETRY"))
    print(f"Tentativa número: {retry_count}")
    cards = client.get_cards_by_rarity('Special')
    if retry_count < possible_retries:
        time.sleep(5)
    print("Busca especial finalizada")
    return cards
