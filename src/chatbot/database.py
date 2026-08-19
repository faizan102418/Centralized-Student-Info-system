"""MySQL access layer: connects to the database and assembles per-student records."""

import mysql.connector

from chatbot.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


def get_db_connection() -> mysql.connector.MySQLConnection:
    """Open and return a new MySQL connection."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        return connection
    except mysql.connector.Error as exc:
        raise RuntimeError(f"Could not connect to MySQL database '{DB_NAME}': {exc}") from exc


def fetch_student_data_from_db() -> str:
    """
    Fetch and merge student data from the general, scholarship, and fee
    tables, keyed by student name, and return it as newline-separated text
    ready to be chunked and embedded.

    Note: joining on name is fine for a small demo/FYP dataset but is not
    collision-safe for two students who share a name. A production version
    should join on a stable student ID instead.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT roll_number, name, discipline FROM student_general_data")
        general_data = {row["name"].lower(): row for row in cursor.fetchall()}

        cursor.execute("SELECT name, scholarship_name, enrollment_status FROM student_scholarship")
        scholarship_data = {row["name"].lower(): row for row in cursor.fetchall()}

        cursor.execute("SELECT registration_number, name, fee_status FROM student_fee_submission")
        fee_data = {row["name"].lower(): row for row in cursor.fetchall()}

        all_names = set(general_data) | set(scholarship_data) | set(fee_data)
        records = []

        for name_key in all_names:
            parts = []

            if gd := general_data.get(name_key):
                parts.append(f"Student Name: {gd.get('name')}")
                if gd.get("roll_number"):
                    parts.append(f"Roll Number: {gd.get('roll_number')}")
                if gd.get("discipline"):
                    parts.append(f"Discipline: {gd.get('discipline')}")

            if sd := scholarship_data.get(name_key):
                if sd.get("scholarship_name"):
                    parts.append(f"Scholarship Name: {sd.get('scholarship_name')}")
                if sd.get("enrollment_status"):
                    parts.append(f"Scholarship Enrollment Status: {sd.get('enrollment_status')}")

            if fd := fee_data.get(name_key):
                if fd.get("registration_number"):
                    parts.append(f"Registration Number: {fd.get('registration_number')}")
                if fd.get("fee_status"):
                    parts.append(f"Fee Status: {fd.get('fee_status')}")

            if parts:
                records.append(" -- ".join(parts))

        return "\n\n".join(records)

    except Exception as exc:
        raise RuntimeError(f"Failed to fetch student data: {exc}") from exc
    finally:
        if connection is not None and connection.is_connected():
            connection.close()
