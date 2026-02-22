import logging
import re

logger = logging.getLogger(__name__)

def cleanup(rows):
    cleaned_rows = stripAllRows(rows)
    cleaned_rows = removeEmptyRows(cleaned_rows)
    cleaned_rows = toLowerCase(cleaned_rows)
    cleaned_rows = dropFirstNonDateColumn(cleaned_rows)
    return cleaned_rows

def stripAllRows(rows):
    cleaned_rows = []
    for row in rows:
        cleaned_row = []
        for cell in row:
            if cell is not None:
                cleaned_cell = cell.strip()
                cleaned_row.append(cleaned_cell)
            else:
                cleaned_row.append("")
        cleaned_rows.append(cleaned_row)
    return cleaned_rows

def removeEmptyRows(rows):
    cleaned_rows = []
    for row in rows:
        if not all(cell == "" for cell in row):
            cleaned_rows.append(row)
        else:
            logger.debug(f"Removed empty row: {row}")
    return cleaned_rows

def toLowerCase(rows):
    for row in rows:
        for i in range(len(row)):
            row[i] = row[i].lower()
    return rows

def dropFirstNonDateColumn(rows):
    # drop a cell in a row if the cell does not contain pattern Dec31
    for row in rows:
        logger.debug(f"Checking row for dropping first cell: {row}")
        if not re.match(r".*[a-zA-Z]{3}\d{1,2}.*", row[0].strip()):
            logger.debug(f"Dropping first cell in row: {row}")
            row.remove(row[0])
                
    return rows