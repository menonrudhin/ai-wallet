from prophet import Prophet
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def forecast_category(monthly_df, category, periods=12):
    cat_df = monthly_df[monthly_df["category"] == category]

    if len(cat_df) < 6:
        logger.debug(f"Not enough data for {category}")
        return None

    prophet_df = cat_df[["month", "amount"]].copy()
    prophet_df.columns = ["ds", "y"]

    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(prophet_df)

    future = model.make_future_dataframe(periods=periods, freq="ME")
    forecast = model.predict(future)

    return forecast[["ds", "yhat"]].tail(periods)

def predict_next_year(df):
    logger.debug(f"Before forecasting, dataframe is: \n{df.head()}")
    # ensure date column is datetime; specify format if not already
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    df["amount"] = df["amount"].astype(str).str.replace(",", "").apply(pd.to_numeric, errors="coerce")
    logger.debug("Sample amounts before filtering:")
    logger.debug(df[["category", "amount"]].head(20))

    df["month"] = df["date"].dt.to_period("M")

    monthly = (
        df.groupby(["month", "category"])["amount"]
        .sum()
        .reset_index()
    )

    monthly["month"] = monthly["month"].dt.to_timestamp()

    categories = monthly["category"].unique()

    all_forecasts = {}

    for cat in categories:
        logger.debug(f"Forecasting for category: {cat}")
        forecast = forecast_category(monthly, cat)
        if forecast is not None:
            all_forecasts[cat] = forecast
            logger.debug(f"Forecast for category: {cat} is {forecast['yhat'].sum()}")

    total_next_year = 0

    for cat, forecast_df in all_forecasts.items():
        total_next_year += forecast_df["yhat"].sum()

    logger.debug(f"Predicted Total Expense Next Year: {round(total_next_year, 2)}")
    return total_next_year