import logging

logger = logging.getLogger(__name__)

def cleanup(rows):
    cleaned_rows = stripAllRows(rows)
    cleaned_rows = removeEmptyRows(cleaned_rows)
    cleaned_rows = toLowerCase(cleaned_rows)
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