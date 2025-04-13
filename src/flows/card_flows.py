from prefect import flow
from src.tasks.card_tasks import search_cards, search_specific_card, search_special_rarity

@flow(log_prints=True)
def project(name="Project External API"):
    data = search_cards()
    search_specific_card(data)
    data_special = search_special_rarity()
    search_specific_card(data_special)
    return "Processo concluído com sucesso!"