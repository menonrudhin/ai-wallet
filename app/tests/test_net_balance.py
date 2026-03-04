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

    def test_net_by_transactions(self):
        from net_balance import net_by_transactions
        from transaction_model import TransactionModel

        # debit then credit -> net negative
        t1 = TransactionModel("2025-01-01", "foo", "100.00", "")
        t1.type = "Debit"
        t2 = TransactionModel("2025-01-02", "bar", "50.00", "")
        t2.type = "Credit"
        self.assertEqual(net_by_transactions([t1, t2]), -50.00)

        # comma and integer handling
        t3 = TransactionModel("2025-01-03", "baz", "1,000.00", "")
        t3.type = "Debit"
        t4 = TransactionModel("2025-01-04", "qux", "500", "")
        t4.type = "Credit"
        self.assertEqual(net_by_transactions([t3, t4]), -500.00)

    def test_net_by_transactions(self):
        from net_balance import net_by_transactions
        from transaction_model import TransactionModel

        # debit then credit -> net negative
        t1 = TransactionModel("2025-01-01", "foo", "100.00", "")
        t1.type = "Debit"
        t2 = TransactionModel("2025-01-02", "bar", "50.00", "")
        t2.type = "Credit"
        self.assertEqual(net_by_transactions([t1, t2]), -50.00)

        # comma and integer handling
        t3 = TransactionModel("2025-01-03", "baz", "1,000.00", "")
        t3.type = "Debit"
        t4 = TransactionModel("2025-01-04", "qux", "500", "")
        t4.type = "Credit"
        self.assertEqual(net_by_transactions([t3, t4]), -500.00)