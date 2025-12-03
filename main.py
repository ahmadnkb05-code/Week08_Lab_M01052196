from app.data.db import connect_database
from app.data.schema import create_all_tables
from app.services.user_service import register_user, login_user, migrate_users_from_file
from app.data.incidents import (
    insert_incident, get_all_incidents, load_incidents_from_csv,
    update_incident_status, delete_incident, get_open_incidents, get_summary_report
)
from app.data.datasets import load_datasets_from_csv
from app.data.tickets import load_tickets_from_csv


def main():
    print("=" * 60)
    print("Week 8 Lab: Hybrid database")
    print("=" * 60)

    # 1️. Database setup
    conn = connect_database()
    create_all_tables(conn)
    conn.close()
    print("✅ Database and tables ready\n")

    # 2️. User operations
    print(migrate_users_from_file())
    ok, msg = register_user("alice", "SecurePass123!", "analyst")
    print(msg)
    ok, msg = login_user("alice", "SecurePass123!")
    print(msg)

    # 3️. Load CSV data
    print(load_incidents_from_csv())
    print(load_datasets_from_csv())
    print(load_tickets_from_csv())

    # 4️. Add new incident
    incident_id = insert_incident(
        "2025-12-03", "Phishing", "High", "Open",
        "Suspicious email detected from external domain", "alice"
    )
    print(f"🧾 Created incident #{incident_id}")

    # 5️. Update and Delete Demo
    print(update_incident_status(incident_id, "Closed"))
    print(delete_incident(1))  # deletes incident #1 just for demo

    # 6️. Show only open incidents
    print("\n Open Incidents:")
    df_open = get_open_incidents()
    print(df_open)

    # 7️. Show summary report
    print("\n Summary Report (Incidents by Type & Severity):")
    print(get_summary_report())

    # 8️. Show all incidents (final state)
    print("\n All Incidents:")
    print(get_all_incidents())


if __name__ == "__main__":
    main()
