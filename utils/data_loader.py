import pandas as pd
from app.config import DATA_PATH


def load_data():
    df = pd.read_csv(DATA_PATH)
    return df