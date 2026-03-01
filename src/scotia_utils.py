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
            
def extract_date(row, year):
    logger.debug(f"Extracting date from row: {row} with year: {year}")
    # extract date in format MonthDay,Year from row
    match = re.search(r"(^[a-zA-Z]{3}\d{1,2})", row)
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
        logger.debug(f"No date found in row: {row}")
        return None
    
def extract_description(row):
    # if any cell has string "openingbal" or "closingbal" then skip the row
    if "openingbal" in row.lower() or "closingbal" in row.lower():
        return None

    logger.debug(f"Extracting description from row: {row}")
    if (row.strip() != "") and (not re.match(r"\${0,1}\d{1,3}(,\d{3})*(\.\d{2})?", row.strip())):
        # extract only the non-numeric part of the string as description
        desc = re.sub(r"\${0,1}\d{1,3}(,\d{3})*(\.\d{2})?", "", row).strip()
        # remove first four characters if they are in format "feb "
        if re.match(r"^[a-zA-Z]{3}\s", desc):
            desc = desc[4:]
        logger.debug(f"Extracted description row: {desc}")
    return desc.strip()


def extract_transaction_amount(row):
    all_matches = []
    matches = re.finditer(r"\d{1,3}(,\d{3})*(\.\d{2})?", row.strip())
    temp = ""
    # ignore first match
    first_match = True
    for match in matches:
        logger.debug(f"Found transaction amount match: {match.group(0)} in row: {row}")
        if first_match:
            first_match = False
            continue
        if not "." in match.group(0):
            temp = match.group(0)
        elif temp != "" and "." in match.group(0):
            all_matches.append(temp + match.group(0))
            temp = ""
        else:
            temp = ""
            all_matches.append(match.group(0))
        logger.debug(f"All matches so far: {all_matches}")
    max = len(all_matches)
    if max > 1:
        return all_matches[max-2]
    return None

def extract_balance(row):
    # find all numeric amounts in the row and return the second one
    all_matches = []
    matches = re.finditer(r"\d{1,3}(,\d{3})*(\.\d{2})?", row.strip())
    for match in matches:
        logger.debug(f"Found balance match: {match.group(0)} in row: {row}")
        all_matches.append(match.group(0))
    max = len(all_matches)
    if max > 1:
        return all_matches[max-1]
    return None

def merge_rows(transactions):
    merged_rows = []
    for transaction in transactions:
        merged_row = " ".join(transaction)
        merged_rows.append(merged_row)

    for merged_row in merged_rows:
        logger.debug(f"Merged Row: {merged_row}")
    
    return merged_rows

def extract_additional_description(merged_rows):
    pattern = re.compile(r"(^[a-zA-Z]{3}\d{1,2})")  # Pattern to match lines starting with a word followed by 2 digits (e.g., jan31)
    new_merged_rows = []
    i = 0
    while i < len(merged_rows):
        current_row = merged_rows[i]
        if pattern.match(current_row.strip()):
            logger.debug(f"Transaction start with date: {current_row} at index: {i}")
            combined_row = current_row.strip()
            i += 1
            while i < len(merged_rows) and not pattern.match(merged_rows[i].strip()) and merged_rows[i].strip() != "":
                logger.debug(f"Appending row: {merged_rows[i]} to current transaction: {combined_row}")
                combined_row += " " + merged_rows[i].strip()
                i += 1
            logger.debug(f"Combined transaction row: {combined_row}")
            new_merged_rows.append(combined_row)
        else:
            new_merged_rows.append(current_row)
            i += 1
    return new_merged_rows

def net_by_transactions(transaction_obj_list):
    net_balance_by_transactions = 0
    for transaction in transaction_obj_list:
        # Convert amount to numeric (remove commas if present)
        amount = float(str(transaction.amount).replace(",", ""))
        if transaction.type == "Debit":
            logger.debug(f"Processing Debit Transaction: {transaction} , Amount: {amount}")
            net_balance_by_transactions -= amount
        elif transaction.type == "Credit":
            logger.debug(f"Processing Credit Transaction: {transaction} , Amount: {amount}")
            net_balance_by_transactions += amount

    return round(net_balance_by_transactions, 2)

def cleanup(rows):
    cleaned_rows = []
    for row in rows:
        cleaned_row = [cell.strip() for cell in row]
        cleaned_rows.append(cleaned_row)
    return cleaned_rows