import unittest
from scotia_cleanup import cleanup


class TestCleanup(unittest.TestCase):
    def test_cleanup_strips_whitespace(self):
        rows = [["  hello  ", "  world  "], ["foo", "  bar"]]
        result = cleanup(rows)
        self.assertEqual(result[0][0], "hello")
        self.assertEqual(result[0][1], "world")
        self.assertEqual(result[1][1], "bar")

    def test_cleanup_converts_to_lowercase(self):
        rows = [["HELLO", "WoRLd"], ["FOO", "Bar"]]
        result = cleanup(rows)
        self.assertEqual(result[0][0], "hello")
        self.assertEqual(result[0][1], "world")
        self.assertEqual(result[1][0], "foo")
        self.assertEqual(result[1][1], "bar")

    def test_cleanup_removes_empty_rows(self):
        rows = [["hello", "world"], ["", ""], ["foo", "bar"]]
        result = cleanup(rows)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["hello", "world"])
        self.assertEqual(result[1], ["foo", "bar"])

    def test_cleanup_handles_none_values(self):
        rows = [["hello", None], [None, "world"]]
        result = cleanup(rows)
        self.assertEqual(result[0][0], "hello")
        self.assertEqual(result[0][1], "")
        self.assertEqual(result[1][0], "")
        self.assertEqual(result[1][1], "world")

    def test_cleanup_combined_operations(self):
        rows = [["  HELLO  ", "  WORLD  "], ["", ""], ["  FOO  ", "  BAR  "]]
        result = cleanup(rows)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], ["hello", "world"])
        self.assertEqual(result[1], ["foo", "bar"])

    def test_cleanup_with_already_clean_data(self):
        rows = [["hello", "world"], ["foo", "bar"]]
        result = cleanup(rows)
        self.assertEqual(result, [["hello", "world"], ["foo", "bar"]])


if __name__ == '__main__':
    unittest.main()