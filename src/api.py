from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import shutil
import os
import tempfile
import pandas as pd
import logging
import matplotlib
# use non-interactive backend to avoid GUI errors in threads
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

from file_reader import read_file
from scotia_utils import cleanup, opening_balance, closing_balance, extract_year
from statement_to_model_mapper import map_statement_to_model
from ml_analysis import ml_analyze
from plot_chart import plot_pie_chart, plot_bar_chart
from forcast.forcast_category import predict_next_year

app = FastAPI()
logger = logging.getLogger(__name__)


def process_files(file_paths):
    """
    Given a list of full paths to statement PDF files, process them and
    return a bytes object representing a PDF report.
    """
    overall_net_balance = 0
    transactions = []
    year = None

    # Read and clean each statement; assume filename identifies statement
    for path in file_paths:
        directory, fname = os.path.split(path)
        rows = read_file(directory, fname)
        rows = cleanup(rows)
        transactions.extend(rows)
        start = opening_balance(rows)
        close = closing_balance(rows)
        year = extract_year(rows)
        net_balance = 0
        if start is not None and close is not None:
            net_balance = float(str(close).replace("$", "").replace(",", "")) - float(str(start).replace("$", "").replace(",", ""))
        overall_net_balance += net_balance

    # merge and extract additional description is performed in analyzer; replicate here
    from scotia_utils import merge_rows, extract_additional_description, net_by_transactions

    merged_rows = merge_rows(transactions)
    transactions = extract_additional_description(merged_rows)

    transaction_obj_list = []
    for transaction in transactions:
        txn_obj = map_statement_to_model(transaction, year)
        if txn_obj is not None:
            transaction_obj_list.append(txn_obj)

    analysis_df, transaction_obj_list = ml_analyze(transaction_obj_list)

    net_balance_by_transactions = net_by_transactions(transaction_obj_list)

    # prepare forecast
    total_next_year = predict_next_year(analysis_df)

    # generate PDF report in memory
    buffer = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    try:
        with PdfPages(buffer.name) as pdf:
            # summary page
            fig, ax = plt.subplots()
            ax.axis("off")
            text = (
                f"Overall Net Balance for the year: {round(overall_net_balance, 2)}\n"
                f"Net Balance calculated from transactions: {round(net_balance_by_transactions, 2)}"
            )
            ax.text(0.1, 0.5, text, fontsize=12)
            pdf.savefig(fig)
            plt.close(fig)

            # pie chart page
            fig = plot_pie_chart(analysis_df, return_fig=True)
            pdf.savefig(fig)
            plt.close(fig)

            # bar chart page
            fig = plot_bar_chart(analysis_df, return_fig=True)
            pdf.savefig(fig)
            plt.close(fig)

            # forecast page
            fig, ax = plt.subplots()
            ax.axis("off")
            lines = ["Forecasted total next year:", str(total_next_year)]
            ax.text(0.1, 0.9, "\n".join(lines), fontsize=10)
            pdf.savefig(fig)
            plt.close(fig)

        buffer.seek(0)
        return open(buffer.name, "rb")
    finally:
        # the file will be removed after streaming response closes
        pass


@app.post("/upload")
def upload_pdfs(files: list[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    temp_dir = tempfile.mkdtemp()
    saved_paths = []
    try:
        for upload in files:
            file_location = os.path.join(temp_dir, upload.filename)
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(upload.file, buffer)
            saved_paths.append(file_location)

        report_file = process_files(saved_paths)
        return StreamingResponse(report_file, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})
    finally:
        # cleanup temp files
        for p in saved_paths:
            try:
                os.remove(p)
            except Exception:
                pass
        try:
            os.rmdir(temp_dir)
        except Exception:
            pass
