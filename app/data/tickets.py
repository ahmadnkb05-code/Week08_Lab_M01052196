import pandas as pd
from app.data.db import connect_database

def load_tickets_from_csv(csv_path='DATA/it_tickets.csv'):
    """Load IT support tickets from a csv file"""
    conn = connect_database()
    df = pd.read_csv(csv_path)
    df.to_sql('it_tickets', conn, if_exists='append', index=False)
    n = len(df)
    conn.close()
    return f"Loaded {n} IT tickets from CSV."
