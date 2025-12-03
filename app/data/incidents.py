import pandas as pd
from app.data.db import connect_database


# Create / Insert Operations
def insert_incident(date, incident_type, severity, status, description, reported_by=None):
    conn = connect_database()
    c = conn.cursor()
    c.execute("""
        INSERT INTO cyber_incidents (date, incident_type, severity, status, description, reported_by)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (date, incident_type, severity, status, description, reported_by))
    conn.commit()
    incident_id = c.lastrowid
    conn.close()
    return incident_id


# Read Operations
def get_all_incidents():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM cyber_incidents ORDER BY id DESC", conn)
    conn.close()
    return df


def get_open_incidents():
    """Return only the open incidents"""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT * FROM cyber_incidents WHERE status = 'Open' ORDER BY id DESC", conn)
    conn.close()
    return df


# Update Operations
def update_incident_status(incident_id, new_status):
    """Change the status of an incident (for example: Open → Closed)"""
    conn = connect_database()
    c = conn.cursor()
    c.execute(
        "UPDATE cyber_incidents SET status = ? WHERE id = ?",
        (new_status, incident_id)
    )
    conn.commit()
    conn.close()
    return f"✅ Incident #{incident_id} updated to '{new_status}'."


# Delete Operations
def delete_incident(incident_id):
    """Remove an incident from the database"""
    conn = connect_database()
    c = conn.cursor()
    c.execute("DELETE FROM cyber_incidents WHERE id = ?", (incident_id,))
    conn.commit()
    conn.close()
    return f"🗑️ Incident #{incident_id} deleted successfully."


# Load from CSV
def load_incidents_from_csv(csv_path='DATA/cyber_incidents.csv'):
    conn = connect_database()
    df = pd.read_csv(csv_path)
    df.to_sql('cyber_incidents', conn, if_exists='append', index=False)
    n = len(df)
    conn.close()
    return f"Loaded {n} incidents from CSV."


# Reporting Utilities
def get_summary_report():
    """Show total incidents by severity and type"""
    conn = connect_database()
    df = pd.read_sql_query(
        "SELECT incident_type, severity, COUNT(*) as total "
        "FROM cyber_incidents GROUP BY incident_type, severity", conn)
    conn.close()
    return df
