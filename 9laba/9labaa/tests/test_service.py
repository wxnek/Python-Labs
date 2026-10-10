import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from exceptions import CalculationError
from repository import CalculationRepository
from service import Service


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = Service(CalculationRepository())

    def test_calculate(self):
        result = self.service.calculate("15 * 4 + 2")
        self.assertEqual(result.result, 62.0)

    def test_division_by_zero(self):
        with self.assertRaises(CalculationError):
            self.service.calculate("10 / 0")
