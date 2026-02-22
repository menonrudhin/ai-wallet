import unittest
from unittest.mock import patch, MagicMock
import file_reader

class TestNetBalance(unittest.TestCase):
    def test_net_balance_monthly(self):
        from net_balance import net_balance_monthly
        opening = "$1,000.00"
        closing = "$1,500.00"
        expected_net_balance = 500.00
        self.assertEqual(net_balance_monthly(opening, closing), expected_net_balance)