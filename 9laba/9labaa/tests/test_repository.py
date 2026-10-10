import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from models import Calculation
from repository import CalculationRepository


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.repository = CalculationRepository()

    def test_add_and_get(self):
        item = Calculation(1, "2 + 2", 4.0, "2026-10-05T12:00:00")
        self.repository.add(item)
        self.assertEqual(self.repository.get(1), item)

    def test_delete(self):
        item = Calculation(1, "2 + 2", 4.0, "2026-10-05T12:00:00")
        self.repository.add(item)
        self.assertTrue(self.repository.delete(1))
        self.assertIsNone(self.repository.get(1))
