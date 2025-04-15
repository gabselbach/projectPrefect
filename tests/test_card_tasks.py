"""Teste de cada Task"""

import unittest
from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock
import json
import os 

patch("prefect.task", lambda **kwargs: lambda func: func).start()
patch("prefect.logging.get_logger", Mock()).start()

from src.tasks.card_tasks import search_cards
from src.tasks.card_tasks import search_specific_card
from src.tasks.card_tasks import search_special_rarity


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

    @patch("src.tasks.card_tasks.client")
    @patch("src.tasks.card_tasks.logger")
    def test_search_specific_card(self, mock_logger, mock_client):
        """Testa se a tarefa search_specific_card retorna o card específico corretamente."""
        mock_card = {"id": 1, "name": "Card 1", "rarity": "Commom"}
        mock_client.get_card_by_id.return_value = mock_card
        input_data = [
            {"id": 1, "name": "Card 1", "rarity": "Commom"},
            {"id": 2, "name": "Card 2", "rarity": "Rare"},
            {"id": 3, "name": "Card 3", "rarity": "Mythic"},
        ]

        result = search_specific_card(input_data)


        self.assertEqual(result, mock_card)
        mock_client.get_card_by_id.assert_called_once_with(1)
        mock_logger.info.assert_any_call("Card específico:")
        mock_logger.info.assert_any_call("Name: %s", mock_card["name"])

    @patch('src.tasks.card_tasks.client')
    @patch('src.tasks.card_tasks.logger')
    @patch('src.tasks.card_tasks.context.get_run_context')
    @patch('src.tasks.card_tasks.time.sleep')
    @patch.dict(os.environ, {"QT_RETRY": "2"})
    def test_search_special_rarity_first_attempt(self, mock_sleep, mock_context, mock_logger, mock_client):
        """Testa se a tarefa search_special_rarity funciona na primeira tentativa."""
        mock_special_cards = [
            {"id": 1, "name": "Card 1", "rarity": "Special"},
            {"id": 2, "name": "Card 2", "rarity": "Special"},
             {"id": 3, "name": "Card 3", "rarity": "Special"},
        ]
        mock_client.get_cards_by_rarity.return_value = mock_special_cards
        mock_run_context = MagicMock()
        mock_run_context.task_run.run_count = 1
        mock_context.return_value = mock_run_context
        
        rarity = "Special"
        result = search_special_rarity(rarity)
        
        self.assertEqual(result, mock_special_cards)
        mock_client.get_cards_by_rarity.assert_called_once_with(rarity)
        mock_logger.info.assert_any_call("Tentativa número: %d ", 1)
        mock_logger.info.assert_any_call("Busca especial finalizada")
        mock_sleep.assert_called_once_with(5)

    @patch('src.tasks.card_tasks.client')
    @patch('src.tasks.card_tasks.logger')
    @patch('src.tasks.card_tasks.context.get_run_context')
    @patch('src.tasks.card_tasks.time.sleep')
    @patch.dict(os.environ, {"QT_RETRY": "2"})
    def test_search_special_rarity_last_attempt(self, mock_sleep, mock_context, mock_logger, mock_client):
        """Testa se a tarefa search_special_rarity funciona na última tentativa."""
        mock_special_cards = [
            {"id": 1, "name": "Card 1", "rarity": "Rare"},
            {"id": 2, "name": " Card 2", "rarity": "Special"}
        ]
        mock_client.get_cards_by_rarity.return_value = mock_special_cards
        mock_run_context = MagicMock()
        mock_run_context.task_run.run_count = 2
        mock_context.return_value = mock_run_context
        
        rarity = "Rare"
        result = search_special_rarity(rarity)
        
        self.assertEqual(result, mock_special_cards)
        mock_client.get_cards_by_rarity.assert_called_once_with(rarity)
        mock_logger.info.assert_any_call("Tentativa número: %d ", 2)
        mock_logger.info.assert_any_call("Busca especial finalizada")
        mock_sleep.assert_not_called()