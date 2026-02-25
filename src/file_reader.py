import pdfplumber
import logging

table_setting = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text"
}

logger = logging.getLogger(__name__)

def read_file(pdf_path, statement):
    rows = []
    with pdfplumber.open(pdf_path + statement) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables(table_settings=table_setting)
            for table in tables:
                for row in table:
                    logger.debug(row)
                    rows.append(row)
    return rows