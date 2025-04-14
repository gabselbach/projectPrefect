"""Este módulo fornece funções para buscar informações sobre cards de um jogo.

Ele se conecta a uma API externa e retorna dados sobre cards,
com base em diferentes critérios, como raridade, conjunto e nome.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class CardSearchError(requests.exceptions.RequestException):
    """Exceção personalizada para erros ao buscar cards.
    """

class CardClient:
    """Uma classe para interagir com uma API de cards.

    Esta classe encapsula a lógica para fazer requisições HTTP para uma API de cards
    ,permitindo buscar todos os cards, um card específico por ID e cards por raridade.

    Attributes:
        base_url (str): A URL base da API.
    """
    def __init__(self):
        """Inicializa uma nova instância da classe CardClient.

        A URL base da API deve ser definida na variável de ambiente URL_API.
        Se a variável de ambiente não estiver definida, 
        uma exceção ValueError será levantada.
        """
        self.base_url = os.environ.get("URL_API")
        if not self.base_url:
            raise ValueError("URL_API não encontrada nas variáveis de ambiente")
        
    def get_all_cards(self):
        """Busca todos os cards disponíveis na API.

        Returns:
            list: Uma lista de dicionários, onde cada dicionário representa um card.

        Raises:
            Exception: Se ocorrer um erro durante a requisição HTTP.
        """
        url = f'{self.base_url}/cards'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()['cards']
        except requests.exceptions.RequestException as e:
            raise CardSearchError(f"Erro ao buscar os cards: {e}") from e

    def get_card_by_id(self, card_id: int):
        """Busca um card específico na API pelo seu ID.

        Args:
            card_id (int): O ID do card a ser buscado.

        Returns:
            dict: Um dicionário representando o card encontrado.

        Raises:
            Exception: Se ocorrer um erro durante a requisição HTTP.
        """
        url = f'{self.base_url}/cards/{card_id}'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status() 
            return response.json()['card']
        except requests.exceptions.RequestException as e:
            raise CardSearchError(f"Erro ao buscar o card específico: {e}") from e
    def get_cards_by_rarity(self, rarity: str):
        """Busca cards com uma raridade específica na API.

        Args:
            rarity (str): A raridade dos cards a serem buscados.

        Returns:
            list: Uma lista de dicionários, onde cada dicionário representa um card 
            com a raridade especificada.

        Raises:
            Exception: Se ocorrer um erro durante a requisição HTTP.
        """
        url = f'{self.base_url}/cards'
        params = {'rarity': rarity}
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()['cards']
        except requests.exceptions.RequestException as e:
            raise CardSearchError(f"Erro ao buscar cards por raridade: {e}") from e
