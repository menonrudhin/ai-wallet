import unittest
from datetime import datetime
from scotia_utils import extract_balance, extract_date, extract_description, extract_transaction_amount, extract_year, opening_balance, closing_balance, merge_rows, extract_additional_description

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
        self.assertEqual(result, datetime(2024, 10, 31, 0, 0))

    def test_extract_description_1(self):
        row = 'jan13 health/dentalclaimins 68.40 16,753.11 '
        result = extract_description(row)
        self.assertEqual(result, "health/dentalclaimins")

    def test_extract_description_2(self):
        row = 'jan30 mortgagepa yment2,495.06 19,452.12'
        result = extract_description(row)
        self.assertEqual(result, "mortgagepa yment")

    def test_extract_transaction_amount_1(self):
        row = 'jan30mortgagepa yment 2,495.0619,452.12'
        result = extract_transaction_amount(row)
        self.assertEqual(result, "2,495.06")

    def test_extract_transaction_amount_2(self):
        row = 'jan30 payrolldep. 3,977.3621,947.18'
        result = extract_transaction_amount(row)
        self.assertEqual(result, "3,977.36")

    def test_extract_transaction_amount_3(self):
        row = 'jan9 1,000.00 17,960.71'
        result = extract_transaction_amount(row)
        self.assertEqual(result, "1,000.00")

    def test_extract_transaction_amount_4(self):
        row = 'jan9 deposit1,000.00 17,960.71 675.00'
        result = extract_balance(row)
        self.assertEqual(result, "675.00")

    def test_merge_rows_and_additional_description(self):
        transactions = [["jan1", "food"], ["extra line"], ["feb2", "rent"], ["more"]]
        merged = merge_rows(transactions)
        # each inner list becomes single string
        self.assertEqual(merged, ["jan1 food", "extra line", "feb2 rent", "more"])

        # now feed merged into extract_additional_description
        extended = extract_additional_description(merged)
        # second item should be appended to first transaction until new date pattern
        self.assertEqual(extended, ["jan1 food extra line", "feb2 rent more"])    

if __name__ == '__main__':
    unittest.main()