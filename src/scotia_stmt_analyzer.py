import re
import time
import sys
import logging
from file_reader import read_file
from ml_analysis import ml_analyze
from plot_chart import plot_bar_chart, plot_pie_chart
from scotia_utils import opening_balance, closing_balance, extract_year
from net_balance import net_balance_monthly
from scotia_cleanup import cleanup
from statement_to_model_mapper import map_statement_to_model

if (len(sys.argv) < 2):
    print("Error: No file path provided")
    sys.exit(1)

file_path = sys.argv[1]

statements = ["jan.pdf","feb.pdf","mar.pdf","apr.pdf","may.pdf", "jun.pdf", "jul.pdf", "aug.pdf",
              "sep.pdf", "oct.pdf", "nov.pdf", "dec.pdf"]

statements = ["jan.pdf"]

logging.basicConfig(
    level=logging.INFO,
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

merged_rows = []
for row in transactions:
    merged_row = " ".join(row)
    merged_rows.append(merged_row)

for merged_row in merged_rows:
    logger.debug(f"Merged Row: {merged_row}")

transactions = merged_rows

transaction_obj_list = []

for transaction in transactions:
    logger.debug(f"Transaction: {transaction}")
    transaction_obj = map_statement_to_model(transaction, year)
    if transaction_obj is not None:
        logger.info(f"Mapped Transaction: {transaction_obj}")
        transaction_obj_list.append(transaction_obj)

analysis = ml_analyze(transaction_obj_list)

net_balance_by_transactions = 0

for transaction in transaction_obj_list:
    # Convert amount to numeric (remove commas if present)
    amount = float(str(transaction.amount).replace(",", ""))
    if transaction.type == "Debit":
        net_balance_by_transactions -= amount
    elif transaction.type == "Credit":
        net_balance_by_transactions += amount

logger.info(f"Net Balance calculated from transactions: {round(net_balance_by_transactions, 2)}")

plot_pie_chart(analysis[0])
plot_bar_chart(analysis[0])