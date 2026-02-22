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
                    
def extract_year(rows):
    # find pattern on followed by month and day and year in format onMonthDay,Year
    for row in rows:
        for cell in row:
            if "openingbalanceon" in cell:
                year = cell.split(",")[-1]
                return year
            
def extract_date(cell, year):
    # extract date in format MonthDay,Year from cell
    match = re.search(r"([a-zA-Z]{3}\d{1,2}).*", cell)
    if match:
        # convert to yyyy-mm-dd format
        month_name = match.group(1)[:3]
        day = match.group(1)[3:]
        month_map = {
            "jan": "01", "feb": "02", "mar": "03", "apr": "04",
            "may": "05", "jun": "06", "jul": "07", "aug": "08",
            "sep": "09", "oct": "10", "nov": "11", "dec": "12"
        }
        month_number = month_map.get(month_name.lower(), "")
        formatted_date = f"{year}-{month_number}-{day}"
        return formatted_date