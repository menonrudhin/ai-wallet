import re
import pandas as pd
import time
import matplotlib.pyplot as plt
import sys
from file_reader import read_file
from scotia_utils import opening_balance, closing_balance

if (len(sys.argv) < 2):
    print("Error: No file path provided")
    sys.exit(1)

file_path = sys.argv[1]

rows = read_file(file_path)
start = opening_balance(rows)
close = closing_balance(rows)

print(f"Opening Balance: {start}")
print(f"Closing Balance: {close}")