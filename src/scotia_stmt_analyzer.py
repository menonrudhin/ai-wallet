import re
import time
import sys
import logging
from file_reader import read_file
from scotia_utils import opening_balance, closing_balance, extract_year
from net_balance import net_balance_monthly
from scotia_cleanup import cleanup

if (len(sys.argv) < 2):
    print("Error: No file path provided")
    sys.exit(1)

file_path = sys.argv[1]

statements = ["jan.pdf","feb.pdf","mar.pdf","apr.pdf","may.pdf", "jun.pdf", "jul.pdf", "aug.pdf",
              "sep.pdf", "oct.pdf", "nov.pdf", "dec.pdf"]

statements = ["oct.pdf"]

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="app.log",   # logs to file
    filemode="a"          # append mode
)

logger = logging.getLogger(__name__)
overall_net_balance = 0
transactions = []

# Process each statement and calculate net balance
for statement in statements:
    rows = read_file(file_path, statement)
    rows = cleanup(rows)
    transactions.extend(rows)
    start = opening_balance(rows)
    close = closing_balance(rows)
    year = extract_year(rows)
    logger.info(f"Statement Summary for : {statement} , Year: {year}")
    logger.info(f"Opening Balance: {start}")
    logger.info(f"Closing Balance: {close}")
    net_balance = net_balance_monthly(start, close)
    logger.info(f"Net Balance: {net_balance}")
    overall_net_balance += net_balance

logger.info(f"Overall Net Balance for the year: {round(overall_net_balance, 2)}")

for transaction in transactions:
    logger.info(f"Transaction: {transaction}")