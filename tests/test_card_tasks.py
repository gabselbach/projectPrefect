"""Teste de cada Task"""
import unittest
from unittest.mock import patch
import json

from src.tasks.card_tasks import search_cards

class TestCardTasks(unittest.TestCase):
    """Testes para as tarefas relacionadas a cards."""
    @patch("src.tasks.card_tasks.client")
    @patch("src.tasks.card_tasks.logger")
    def test_search_cards(self, mock_logger, mock_client):
        """Testa se a tarefa search_cards retorna os cards corretamente."""
        mock_cards = [
            {"id": 1, "name": "Card 1", "rarity": "Common"},
            {"id": 2, "name": "Card 2", "rarity": "Rare"},
        ]
        mock_client.get_all_cards.return_value = mock_cards
        result = search_cards()
        self.assertEqual(result, mock_cards)
        mock_client.get_all_cards.assert_called_once()
        mock_logger.info.assert_any_call("Pesquisado todos os dados")
        mock_logger.info.assert_any_call(
            json.dumps(mock_cards[0], indent=2, ensure_ascii=False)
        )