import re
import pandas as pd
import time
import matplotlib.pyplot as plt
import sys
from file_reader import read_file
from scotia_utils import opening_balance, closing_balance
from net_balance import net_balance_monthly

if (len(sys.argv) < 2):
    print("Error: No file path provided")
    sys.exit(1)

file_path = sys.argv[1]

statements = ["jan.pdf","feb.pdf","mar.pdf","apr.pdf","may.pdf", "jun.pdf", "jul.pdf", "aug.pdf",
              "sep.pdf", "oct.pdf", "nov.pdf", "dec.pdf"]

overall_net_balance = 0

for statement in statements:
    rows = read_file(file_path, statement)
    start = opening_balance(rows)
    close = closing_balance(rows)
    print(f"Statement Summary for : {statement}")
    print(f"Opening Balance: {start}")
    print(f"Closing Balance: {close}")
    net_balance = net_balance_monthly(start, close)
    print(f"Net Balance: {net_balance}")
    overall_net_balance += net_balance

print(f"Overall Net Balance for the year: {round(overall_net_balance, 2)}")