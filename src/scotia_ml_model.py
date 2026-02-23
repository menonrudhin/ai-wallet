from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd

df = pd.read_csv("training_data.csv")

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression())
])

def initialize_model():
    model.fit(df["description"], df["category"])

def predict_category(descriptions):
    return model.predict(descriptions)