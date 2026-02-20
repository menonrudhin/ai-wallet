import re

def opening_balance(rows):
    # find pattern OpeningBalanceon
    for row in rows:
        # for every cell in row, check if it contains the pattern "OpeningBalanceon"
        for cell in row:
            if "OpeningBalanceon" in cell:
                # for every cell in row, check if the cell starts with $ and number in format x,xxx.xx
                for cell in row:
                    if re.match(r"\$\d{1,3}(,\d{3})*(\.\d{2})?", cell.strip()):
                        return cell

def closing_balance(rows):
    # find pattern ClosingBalanceon
    for row in rows:
        # for every cell in row, check if it contains the pattern "ClosingBalanceon"
        for cell in row:
            if "ClosingBalanceon" in cell:
                # for every cell in row, check if the cell starts with $ and number in format x,xxx.xx
                for cell in row:
                    if re.match(r"\$\d{1,3}(,\d{3})*(\.\d{2})?", cell):
                        return cell