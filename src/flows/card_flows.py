"""Este módulo define um fluxo Prefect para realizar consultas
em uma API externa relacionada a cards.

O fluxo orquestra a busca de todos os cards, a busca de um card específico 
por ID e a busca de cards com uma raridade específica, 
utilizando tarefas definidas em `src.tasks.card_tasks`.
"""
from prefect import flow
from src.tasks.card_tasks import search_cards
from src.tasks.card_tasks import search_specific_card
from src.tasks.card_tasks import search_special_rarity

@flow(log_prints=True)
def project(name: str) -> str:
    """Realiza consultas em API Externa.

    Args:
        name (str): Nome do projeto

    Returns:
        Processo concluído com sucesso!.
    """
    data = search_cards()
    search_specific_card(data)
    data_special = search_special_rarity()
    search_specific_card(data_special)
    return f"{name} processo concluído com sucesso!"
