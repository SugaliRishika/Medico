import sqlite3
import os
from datetime import datetime
import tkinter as tk
from HealthcareDashboard import HealthcareDashboard

class PatientDataManager:
    def __init__(self, db_path='patient_records.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize SQLite database with patient records table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                file_path TEXT NOT NULL,
                upload_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()

    def store_patient_data(self, name, age, file_path):
        """Store patient data in SQLite database"""
        # Validate inputs
        if not name or not age or not file_path:
            raise ValueError("All fields must be provided")

        try:
            age = int(age)
            if age < 0 or age > 120:
                raise ValueError("Invalid age")
        except ValueError:
            raise ValueError("Age must be a valid number between 0 and 120")

        # Ensure file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError("Medical document file not found")

        # Store file in a dedicated directory
        storage_dir = 'patient_documents'
        os.makedirs(storage_dir, exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}{os.path.splitext(file_path)[1]}"
        stored_file_path = os.path.join(storage_dir, filename)

        # Copy file to storage directory
        import shutil
        shutil.copy2(file_path, stored_file_path)

        # Store record in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patient_records 
            (name, age, file_path) 
            VALUES (?, ?, ?)
        ''', (name, age, stored_file_path))
        conn.commit()
        conn.close()
        print("enteredddddddddd")
        return f"Patient {name} record stored successfully"

    def retrieve_patient_records(self):
        """Retrieve all patient records"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patient_records')
        records = cursor.fetchall()
        conn.close()
        return records

# Example usage
def main():
    data_manager = PatientDataManager()
    
    # Simulated patient data storage
    data_manager.store_patient_data(
        name="John Doe", 
        age=35, 
        file_path="/path/to/medical/document.pdf"
    )

    # Retrieve and display records
    records = data_manager.retrieve_patient_records()
    for record in records:
        print(f"Patient: {record[1]}, Age: {record[2]}, File: {record[3]}")
    root = tk.Tk()
    # Create an instance of HealthcareDashboard
    dashboard = HealthcareDashboard(root)
    # Run the tkinter main loop
    root.mainloop()
    
if __name__ == "__main__":
    main()