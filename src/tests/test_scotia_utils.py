import unittest
from scotia_utils import extract_date, extract_description, extract_year, opening_balance, closing_balance

class TestScotiaUtils(unittest.TestCase):
    def test_hello_world(self):
        self.assertEqual(1 + 1, 2)

    def test_opening_balance_found(self):
        rows = [
            ['*0', '', '', '', ''],
            ['0', 'openingbalanceondecember24,2024', '', '$23,677.06', '']
        ]
        self.assertEqual(opening_balance(rows), "$23,677.06")

    def test_opening_balance_not_found(self):
        rows = [
            ['*0', '', '', '', ''],
            ['0', 'omeOtherText24,2024', '', '$23,677.06', '']
        ]
        self.assertIsNone(opening_balance(rows))

    def test_closing_balance_found(self):
        rows = [
            ['', '', '', '', ''],
            ['0', 'closingbalanceonjanuary23,2025', '', '$38,287.77', '']
        ]
        self.assertEqual(closing_balance(rows), "$38,287.77")

    def test_closing_balance_not_found(self):
        rows = [
            ['', '', '', '', ''],
            ['0', 'SomeOtherText24,2025', '', '$38,287.77', '']
        ]
        self.assertIsNone(closing_balance(rows))

    def test_extract_year_found(self):
        rows = [
            ['*0', '', '', '', ''],
            ['0', 'openingbalanceondecember24,2024', '', '$23,677.06', '']
        ]
        self.assertEqual(extract_year(rows), "2024")

    def test_extract_date(self):
        cell = "oct31 description"
        year = "2024"
        result = extract_date(cell, year)
        self.assertEqual(result, "2024-10-31")

    def test_extract_description_1(self):
        row = ['jan13 health/dentalclaimins', '', '68.40 16,753.11', '']
        result = extract_description(row)
        self.assertEqual(result, ["health/dentalclaimins"])

    def test_extract_description_2(self):
        row = ['jan30', 'mortgagepa', 'yment', '2,495.06', '', '19,452.12']
        result = extract_description(row)
        self.assertEqual(result, ["mortgagepa", "yment"])

if __name__ == '__main__':
    unittest.main()