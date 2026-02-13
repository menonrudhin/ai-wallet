import re
import pdfplumber
import pandas as pd
import time
import matplotlib.pyplot as plt

filePathPrefix = "/Users/rudhinmenon/Workspace/python/AI-Wallet/"
statements = ["jan.pdf","feb.pdf","mar.pdf","apr.pdf","may.pdf", "jun.pdf", "jul.pdf", "aug.pdf",
              "sep.pdf", "oct.pdf", "nov.pdf", "dec.pdf"]

table_setting = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text"
}

row_length = 5

def extract_transactions(pdf_path):
    rows = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables(table_settings=table_setting)
            for table in tables:
                for row in table:
                    print(row)

for statement in statements:
    extract_transactions(filePathPrefix + statement);