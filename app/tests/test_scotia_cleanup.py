import unittest
from scotia_cleanup import cleanup


class TestCleanup(unittest.TestCase):
    def test_cleanup_strips_whitespace(self):
        rows = [["  01  ", "  Dec31  "], [" ", "  expense"]]
        result = cleanup(rows)
        self.assertEqual(result[0][0], "dec31")
        self.assertEqual(result[1][0], "expense")

    def test_cleanup_converts_to_lowercase(self):
        rows = [["01", "Dec31 XYZ"], [" 786", "Expense"]]
        result = cleanup(rows)
        self.assertEqual(result[0][0], "dec31 xyz")
        self.assertEqual(result[1][0], "expense")

    def test_cleanup_removes_empty_rows(self):
        rows = [[" x01", " Jan10 PayrollDep."], ["", ""], ["480", " #524867-5 Payment"]]
        result = cleanup(rows)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["jan10 payrolldep."])
        self.assertEqual(result[1], ["#524867-5 payment"])

    def test_cleanup_handles_none_values(self):
        rows = [[" ", None], [None, " YYX"]]
        result = cleanup(rows)
        self.assertEqual(result[0][0], "yyx")

    def test_cleanup_combined_operations(self):
        rows = [["  HELLO  ", "  Dec31deposit  "], ["", ""], ["  FOO  ", "  BAR  "]]
        result = cleanup(rows)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["dec31deposit"])
        self.assertEqual(result[1], ["bar"])

    def test_cleanup_with_already_clean_data(self):
        rows = [["01", "dec31"], ["foo", "yuz"]]
        result = cleanup(rows)
        self.assertEqual(result, [["dec31"], ["yuz"]])


if __name__ == '__main__':
    unittest.main()