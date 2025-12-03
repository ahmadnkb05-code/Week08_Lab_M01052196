import pandas as pd
from app.data.db import connect_database

def load_datasets_from_csv(csv_path='DATA/datasets_metadata.csv'):
    """Load dataset metadata from a csv file"""
    conn = connect_database()
    df = pd.read_csv(csv_path)
    df.to_sql('datasets_metadata', conn, if_exists='append', index=False)
    n = len(df)
    conn.close()
    return f"Loaded {n} datasets from CSV."
