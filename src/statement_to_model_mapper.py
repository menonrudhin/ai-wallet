from transaction_model import TransactionModel
from scotia_utils import extract_date, extract_description
import logging

logger = logging.getLogger(__name__)

def map_statement_to_model(row, year):
    date = extract_date(row[0], year)
    if date is None:
        logger.debug(f"Skipping row due to missing date: {row}")
        return None
    description = extract_description(row)
    if description is None:
        logger.debug(f"Skipping row due to invalid/missing description: {row}")
        return None
    amount = 2.09 #extract_amount(row[2])
    balance = 100.02 #extract_balance(row[3])
    transaction = TransactionModel(date, description, amount, balance)
    logger.info(f"Mapped transaction: {transaction}")
    return transaction