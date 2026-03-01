from scotia_ml_model import initialize_model, predict_category, predict_type
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def ml_analyze(transaction_obj_list):
    # initialize the ML models
    initialize_ml_models()

    # predict categories for transactions
    transaction_obj_list = predict_categories_for_transactions(transaction_obj_list)

    # predict types for transactions
    transaction_obj_list = predict_type_for_transactions(transaction_obj_list)

    # create a dataframe from transaction_obj_list
    df = create_dataframe_from_transactions(transaction_obj_list)

    logger.debug(f"Dataframe after ML analysis: \n{df.head()}")

    return (df,transaction_obj_list)

def create_dataframe_from_transactions(transaction_obj_list):
    # create a dataframe from transaction_obj_list
    df = pd.DataFrame([vars(txn) for txn in transaction_obj_list])
    return df

def initialize_ml_models():
    initialize_model()

def predict_categories_for_transactions(transaction_obj_list):
    descriptions = [" ".join(txn.description) if isinstance(txn.description, list) else txn.description for txn in transaction_obj_list]
    predicted_categories = predict_category(descriptions)

    for txn, category in zip(transaction_obj_list, predicted_categories):
        txn.category = category

    for transaction in transaction_obj_list:
        logger.info(f"Transaction: {transaction} , Predicted Category: {transaction.category}")

    return transaction_obj_list

def predict_type_for_transactions(transaction_obj_list):
    descriptions = [" ".join(txn.description) if isinstance(txn.description, list) else txn.description for txn in transaction_obj_list]

    predicted_types = predict_type(descriptions)

    for txn, txn_type in zip(transaction_obj_list, predicted_types):
        txn.type = txn_type

    return transaction_obj_list