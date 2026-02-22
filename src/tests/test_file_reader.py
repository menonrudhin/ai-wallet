import unittest
from unittest.mock import patch, MagicMock
import file_reader

class TestFileReader(unittest.TestCase):
    @patch("file_reader.pdfplumber.open")
    def test_read_file_returns_rows(self, mock_pdf_open):
        # Mock the PDF and its pages/tables
        mock_pdf = MagicMock()
        mock_page = MagicMock()
        mock_page.extract_tables.return_value = [
            [["cell1", "cell2"], ["cell3", "cell4"]]
        ]
        mock_pdf.pages = [mock_page]
        mock_pdf_open.return_value.__enter__.return_value = mock_pdf

        rows = file_reader.read_file("", "")
        self.assertIsInstance(rows, list)
        self.assertGreater(len(rows), 0)
        self.assertIn(["cell1", "cell2"], rows)

if __name__ == '__main__':
    unittest.main()