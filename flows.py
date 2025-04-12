from prefect import flow, task
import os
import requests

@task(log_prints=True)
def print_data():
    print("Primeira Execução da Task")

@task(log_prints=True)
def search_cards() -> str:
    url = os.environ.get("URL_API")
    response = requests.get(url)
    all_cards = response.json()
    cards = all_cards['cards'] 

    print("Pesquisado todos os dados")
    print(cards[0])
    return cards

@flow(log_prints=True)
def init():
    data = search_cards()

init()