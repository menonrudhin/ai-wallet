from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd

df = pd.read_csv("training_data.csv")

# Pipeline for category prediction
category_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

# Pipeline for transaction type prediction (credit/debit)
type_model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

def initialize_model():
    # Train both models
    category_model.fit(df["description"], df["category"])
    type_model.fit(df["description"], df["type"])  # "credit" or "debit"

def predict_category(descriptions):
    return category_model.predict(descriptions)

def predict_type(descriptions):
    return type_model.predict(descriptions)