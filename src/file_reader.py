import pdfplumber

statements = ["jan.pdf","feb.pdf","mar.pdf","apr.pdf","may.pdf", "jun.pdf", "jul.pdf", "aug.pdf",
              "sep.pdf", "oct.pdf", "nov.pdf", "dec.pdf"]

table_setting = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text"
}

def read_file(pdf_path):
    rows = []
    with pdfplumber.open(pdf_path + statements[0]) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables(table_settings=table_setting)
            for table in tables:
                for row in table:
                    print(row)
                    rows.append(row)
    return rows