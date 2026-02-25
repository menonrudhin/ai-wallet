from transaction_model import TransactionModel
from scotia_utils import extract_balance, extract_date, extract_description, extract_transaction_amount
import logging

logger = logging.getLogger(__name__)

def map_statement_to_model(row, year):
    logger.debug(f"Mapping row to model: {row} for year: {year}")
    if row is None or len(row) == 0:
        logger.debug(f"Skipping empty or None row: {row}")
        return None
    date = extract_date(row, year)
    if date is None:
        logger.debug(f"Skipping row due to missing date: {row}")
        return None
    description = extract_description(row)
    if description is None:
        logger.debug(f"Skipping row due to invalid/missing description: {row}")
        return None
    # TODO issue while extracting amount in following scenario
    # Transaction(date=2025-11-07 00:00:00, description=['mortgagepayment 2,'], amount=495.06, balance=495.06) , Predicted Category: Mortgage
    amount = extract_transaction_amount(row)
    if amount is None:
        logger.debug(f"Skipping row due to missing transaction amount: {row}")
        return None
    balance = extract_balance(row)
    if balance is None:
        logger.debug(f"Skipping row due to missing balance: {row}")
        return None
    transaction = TransactionModel(date, description, amount, balance)
    #logger.info(f"Mapped transaction: {transaction}")
    return transaction