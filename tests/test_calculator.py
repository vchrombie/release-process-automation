from unittest import TestCase
from calculator.calculator import sum


class TestSum(TestCase):
    def test_sum(self):
        result = sum(3, 4)

        self.assertEqual(7, result)
