import requests
import os

from dotenv import load_dotenv

load_dotenv()

class CardClient:
    def __init__(self):
        self.base_url = os.environ.get("URL_API")
        if not self.base_url:
            raise ValueError("URL_API não encontrada nas variáveis de ambiente")
        
    def get_all_cards(self):
        try:
            response = requests.get(f'{self.base_url}/cards')
            return response.json()['cards']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao buscar os cards: {e}")
    
    def get_card_by_id(self, card_id):
        try:
            response = requests.get(f'{self.base_url}/cards/{card_id}')
            return response.json()['card']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao buscar o card específico: {e}")
    
    def get_cards_by_rarity(self, rarity):
        try:
            response = requests.get(f'{self.base_url}/cards?rarity={rarity}')
            return response.json()['cards']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao buscar cards por raridade: {e}")