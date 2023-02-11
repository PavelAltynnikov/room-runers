import unittest

from src.model.level import BoundaryGenerator


class BoundaryGeneratorTests(unittest.TestCase):

    def test_calculate_internal_boundaries_amount_1(self):
        size = 1
        answer = 0

        self.assertEqual(
            BoundaryGenerator._calculate_internal_boundaries_amount(size),  # type: ignore
            answer
        )

    def test_calculate_internal_boundaries_amount_2(self):
        size = 2
        answer = 4

        self.assertEqual(
            BoundaryGenerator._calculate_internal_boundaries_amount(size),  # type: ignore
            answer
        )

    def test_calculate_internal_boundaries_amount_3(self):
        size = 3
        answer = 12

        self.assertEqual(
            BoundaryGenerator._calculate_internal_boundaries_amount(size),  # type: ignore
            answer
        )

    def test_calculate_internal_boundaries_amount_10(self):
        size = 10
        answer = 180

        self.assertEqual(
            BoundaryGenerator._calculate_internal_boundaries_amount(size),  # type: ignore
            answer
        )
