import re
import logging

logger = logging.getLogger(__name__)

def net_balance_monthly(opening_balance, closing_balance):
    # extract float value from string "$34,897.60"
    opening_balance = float(re.sub(r'[^\d.]', '', opening_balance))
    closing_balance = float(re.sub(r'[^\d.]', '', closing_balance))
    # net balance round to 2 decimal places    
    net_balance = round(closing_balance - opening_balance, 2)

    return net_balance

def net_by_transactions(transaction_obj_list):
    net_balance_by_transactions = 0
    for transaction in transaction_obj_list:
        # Convert amount to numeric (remove commas if present)
        amount = float(str(transaction.amount).replace(",", ""))
        if transaction.type == "Debit":
            logger.debug(f"Processing Debit Transaction: {transaction} , Amount: {amount}")
            net_balance_by_transactions -= amount
        elif transaction.type == "Credit":
            logger.debug(f"Processing Credit Transaction: {transaction} , Amount: {amount}")
            net_balance_by_transactions += amount

    return round(net_balance_by_transactions, 2)