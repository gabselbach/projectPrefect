"""Testes sobre a API"""

import os
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock

import requests

from src.api.card_client import CardClient
from src.api.card_client import CardSearchError


class TestCardClient(unittest.TestCase):
    """Testes para a classe CardClient."""

    @patch.dict(os.environ, {"URL_API": "https://google.com"})
    def setUp(self):
        """Configuração para cada teste."""
        self.client = CardClient()

    def test_init_with_url(self):
        """Testa se o construtor inicializa corretamente com URL_API."""
        with patch.dict(os.environ, {"URL_API": "https://google.com"}):
            client = CardClient()
            self.assertEqual(client.base_url, "https://google.com")

    @patch("requests.get")
    def test_get_all_cards_success(self, mock_get):
        """Testa se get_all_cards retorna a lista de cards corretamente."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "cards": [{"id": 1, "name": "Card1"}, {"id": 2, "name": "Card2"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        cards = self.client.get_all_cards()
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["name"], "Card1")
        self.assertEqual(cards[1]["name"], "Card2")

        mock_get.assert_called_once_with(
            f"{self.client.base_url}/cards", timeout=10
        )

    @patch("requests.get")
    def test_get_all_cards_error_connection_error(self, mock_get):
        """Testa se get_all_cards levanta exceção quando há erro na requisição."""
        mock_get.side_effect = requests.exceptions.ConnectionError(
            "Erro de conexão"
        )
        with self.assertRaises(CardSearchError) as context:
            self.client.get_all_cards()
        self.assertIn("Erro ao buscar os cards", str(context.exception))

    @patch("requests.get")
    def test_get_card_by_id_success(self, mock_get):
        """Testa se get_card_by_id retorna o card correto."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"card": {"id": 1, "name": "Card1"}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        card = self.client.get_card_by_id(1)
        self.assertEqual(card["id"], 1)
        self.assertEqual(card["name"], "Card1")
        mock_get.assert_called_once_with(
            f"{self.client.base_url}/cards/1", timeout=10
        )

    @patch("requests.get")
    def test_get_card_by_id_error_not_find(self, mock_get):
        """Testa se get_card_by_id levanta exceção quando há erro na requisição."""
        mock_get.side_effect = requests.exceptions.HTTPError(
            "Card não encontrado"
        )

        with self.assertRaises(CardSearchError) as context:
            self.client.get_card_by_id(999)
        self.assertIn(
            "Erro ao buscar o card específico", str(context.exception)
        )

    @patch("requests.get")
    def test_get_cards_by_rarity_success(self, mock_get):
        """Testa se get_cards_by_rarity retorna a lista de cards correta."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "cards": [
                {"id": 1, "name": "Card1", "rarity": "Special"},
                {"id": 2, "name": "Card2", "rarity": "Special"},
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        cards = self.client.get_cards_by_rarity("Special")
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0]["rarity"], "Special")
        self.assertEqual(cards[1]["rarity"], "Special")

        mock_get.assert_called_once_with(
            f"{self.client.base_url}/cards",
            params={"rarity": "Special"},
            timeout=10,
        )

    @patch("requests.get")
    def test_get_cards_by_rarity_error_timeout(self, mock_get):
        """Testa se get_cards_by_rarity levanta exceção quando há erro na requisição."""
        mock_get.side_effect = requests.exceptions.Timeout("Tempo esgotado")

        with self.assertRaises(CardSearchError) as context:
            self.client.get_cards_by_rarity("Mythic")
        self.assertIn(
            "Erro ao buscar cards por raridade", str(context.exception)
        )
