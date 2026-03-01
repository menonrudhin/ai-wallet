import re
import time
import sys
import logging
import pandas as pd
from file_reader import read_file
from forcast.forcast_category import forecast_category, predict_next_year
from ml_analysis import ml_analyze
from plot_chart import plot_bar_chart, plot_pie_chart
from scotia_utils import extract_additional_description, merge_rows, net_by_transactions, opening_balance, closing_balance, extract_year
from net_balance import net_balance_monthly
from scotia_cleanup import cleanup
from statement_to_model_mapper import map_statement_to_model

if (len(sys.argv) < 2):
    print("Error: No file path provided")
    sys.exit(1)

file_path = sys.argv[1]

statements = ["jan.pdf","feb.pdf","mar.pdf","apr.pdf","may.pdf", "jun.pdf", "jul.pdf", "aug.pdf",
              "sep.pdf", "oct.pdf", "nov.pdf", "dec.pdf"]

#statements = ["dec.pdf"]

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

# Merge all the cells in transactions into a single list of strings
merged_rows = merge_rows(transactions)

# for every row in merged_rows, if the row starts with pattern jan31 then append all the next non empty rows to the current row until we find another row that starts with pattern jan31 or we reach the end of merged_rows
transactions = extract_additional_description(merged_rows)

for merged_row in transactions:
    logger.info(f"New Merged Row: {merged_row}")

# create a list of transaction objects from transactions using map_statement_to_model function and store it in transaction_obj_list
transaction_obj_list = []
for transaction in transactions:
    logger.debug(f"Transaction: {transaction}")
    transaction_obj = map_statement_to_model(transaction, year)
    if transaction_obj is not None:
        logger.debug(f"Mapped Transaction: {transaction_obj}")
        transaction_obj_list.append(transaction_obj)

# ml analysis
analysis = ml_analyze(transaction_obj_list)

net_balance_by_transactions = net_by_transactions(transaction_obj_list)
logger.info(f"Net Balance calculated from transactions: {round(net_balance_by_transactions, 2)}")

# Plot charts
plot_pie_chart(analysis[0])
plot_bar_chart(analysis[0])

# Forcasting
df = analysis[0]
total_next_year = predict_next_year(df)