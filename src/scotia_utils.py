from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

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
    logger.debug(f"Extracting date from cell: {cell} with year: {year}")
    # extract date in format MonthDay,Year from cell
    match = re.search(r"(^[a-zA-Z]{3}\d{1,2})", cell)
    if match:
        # convert to yyyy-mm-dd format
        month_name = match.group(1)[:3]
        day = f"{match.group(1)[3:]}"
        month_map = {
            "jan": "01", "feb": "02", "mar": "03", "apr": "04",
            "may": "05", "jun": "06", "jul": "07", "aug": "08",
            "sep": "09", "oct": "10", "nov": "11", "dec": "12"
        }
        month_number = month_map.get(month_name.lower(), "")
        formatted_date = f"{year}-{month_number}-{day}"
        logger.debug(f"Extracted date: {formatted_date}")
        # create a python date object from formatted_date and return it
        try:
            return datetime.strptime(formatted_date, "%Y-%m-%d")
        except ValueError:
            logger.debug(f"Failed to parse date: {formatted_date}")
            return formatted_date
    else:
        logger.debug(f"No date found in cell: {cell}")
        return None
    
def extract_description(row):
    # for every cell in row extract words and put in an array except the ones that are just numbers
    description = []

    # if any cell has string "openingbal" or "closingbal" then skip the row
    for cell in row:
        if "openingbal" in cell.lower() or "closingbal" in cell.lower():
            return None

    for cell in row:
        logger.debug(f"Extracting description from cell: {cell}")
        if (cell.strip() != "") and (not re.match(r"\${0,1}\d{1,3}(,\d{3})*(\.\d{2})?", cell.strip())):
            # extract only the part that does not have dates like Jan31
            cell = re.sub(r"^[a-zA-Z]{3}\d{1,2}", "", cell)
            logger.debug(f"Extracted description cell: {cell}")
            if cell.strip() != "":
                description.append(cell.strip())
    return description


def extract_transaction_amount(row):
    # for every cell in row, check if the cell has number in format x,xxx.xx, only return the first match
    for cell in row:
        match = re.search(r"(\d{1,3}(,\d{3})*(\.\d{2}))", cell.strip())
        if match:
            return match.group(0)

def extract_balance(row):
    # find all numeric amounts in the row and return the second one
    all_matches = []
    for cell in row:
        matches = re.finditer(r"\d{1,3}(,\d{3})*(\.\d{2})?", cell.strip())
        for match in matches:
            all_matches.append(match.group(0))
    
    if len(all_matches) > 1:
        return all_matches[2]
    return None