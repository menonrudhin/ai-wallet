import logging

logger = logging.getLogger(__name__)

def cleanup(rows):
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

    for row in cleaned_rows:
        # if all cells are empty remove the row
        if all(cell == "" for cell in row):
            cleaned_rows.remove(row)
            logger.debug(f"Removed empty row: {row}")

    for row in cleaned_rows:
        # make all letters lowercase
        for i in range(len(row)):
            row[i] = row[i].lower()
    return cleaned_rows