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

from file_reader import read_file, read_file_api
from scotia_utils import opening_balance, closing_balance, extract_year, merge_rows, extract_additional_description
from scotia_cleanup import cleanup
from statement_to_model_mapper import map_statement_to_model
from ml_analysis import ml_analyze
from net_balance import net_balance_monthly, net_by_transactions
from plot_chart import plot_pie_chart, plot_bar_chart
from forcast.forcast_category import predict_next_year

app = FastAPI()
logger = logging.getLogger(__name__)


def process_files(transactions, year, overall_net_balance):
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
            # prepare forecast
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
    overall_net_balance = 0
    transactions = []
    year = None
    for file in files:
        rows = read_file_api(file)
        rows = cleanup(rows)
        transactions.extend(rows)
        start = opening_balance(rows)
        close = closing_balance(rows)
        year = extract_year(rows)
        net_balance = net_balance_monthly(start, close)
        overall_net_balance += net_balance
    report_file = process_files(transactions, year, overall_net_balance)
    return StreamingResponse(report_file, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=report.pdf"})
