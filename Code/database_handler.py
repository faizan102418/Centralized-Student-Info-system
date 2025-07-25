# database_handler.py
import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_db_connection():
    """Establishes and returns a database connection."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            print(f"✅ Successfully connected to MySQL database: {DB_NAME}")
        return connection
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to MySQL database: {e}")
        raise

def fetch_student_data_from_db():
    """
    Fetches combined student data from all relevant tables.
    Data is combined based on 'name'. This means if multiple students
    have the same name, their data might be combined or one might
    overwrite another based on the dictionary key logic.
    """
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True) # dictionary=True to get results as dicts

        all_student_data = []

        # Fetch general data
        cursor.execute("SELECT roll_number, name, discipline FROM student_general_data")
        general_data = {row['name'].lower(): row for row in cursor.fetchall()}

        # Fetch scholarship data
        cursor.execute("SELECT name, scholarship_name, enrollment_status FROM student_scholarship")
        scholarship_data = {row['name'].lower(): row for row in cursor.fetchall()}

        # Fetch fee submission data
        cursor.execute("SELECT registration_number, name, fee_status FROM student_fee_submission")
        fee_data = {row['name'].lower(): row for row in cursor.fetchall()}

        # Combine data for each student
        # Assuming 'name' is the common identifier across tables for simplicity
        # This approach might lead to ambiguity if different students have the same name.
        all_names = set(general_data.keys()) | set(scholarship_data.keys()) | set(fee_data.keys())

        for name_key in all_names:
            student_record_parts = []
            # This logic tries to get the original case name from any available source
            name = general_data.get(name_key, {}).get('name') or \
                   scholarship_data.get(name_key, {}).get('name') or \
                   fee_data.get(name_key, {}).get('name')

            if general_data.get(name_key):
                gd = general_data[name_key]
                student_record_parts.append(f"Student Name: {gd.get('name')}")
                if gd.get('roll_number'): student_record_parts.append(f"Roll Number: {gd.get('roll_number')}")
                if gd.get('discipline'): student_record_parts.append(f"Discipline: {gd.get('discipline')}")

            if scholarship_data.get(name_key):
                sd = scholarship_data[name_key]
                if sd.get('scholarship_name'): student_record_parts.append(f"Scholarship Name: {sd.get('scholarship_name')}")
                if sd.get('enrollment_status'): student_record_parts.append(f"Scholarship Enrollment Status: {sd.get('enrollment_status')}")

            if fee_data.get(name_key):
                fd = fee_data[name_key]
                if fd.get('registration_number'): student_record_parts.append(f"Registration Number: {fd.get('registration_number')}")
                if fd.get('fee_status'): student_record_parts.append(f"Fee Status: {fd.get('fee_status')}")

            if student_record_parts: # Only add if there's any data
                all_student_data.append(" -- ".join(student_record_parts))

        return "\n\n".join(all_student_data)

    except Exception as e:
        print(f"❌ Error fetching data from database: {e}")
        return ""
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")