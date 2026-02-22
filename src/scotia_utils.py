import re

def opening_balance(rows):
    # find pattern openingbalanceon
    for row in rows:
        # for every cell in row, check if it contains the pattern "openingbalanceon"
        for cell in row:
            if "openingbalanceon" in cell:
                # for every cell in row, check if the cell starts with $ and number in format x,xxx.xx
                for cell in row:
                    if re.match(r"\$\d{1,3}(,\d{3})*(\.\d{2})?", cell.strip()):
                        return cell

def closing_balance(rows):
    # find pattern closingbalanceon
    for row in rows:
        # for every cell in row, check if it contains the pattern "closingbalanceon"
        for cell in row:
            if "closingbalanceon" in cell:
                # for every cell in row, check if the cell starts with $ and number in format x,xxx.xx
                for cell in row:
                    if re.match(r"\$\d{1,3}(,\d{3})*(\.\d{2})?", cell):
                        return cell