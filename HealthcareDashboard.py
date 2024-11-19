import tkinter as tk
from tkinter import filedialog, messagebox
import os

class HealthcareDashboard:
    def __init__(self, master):
        self.master = master
        master.title("Healthcare Patient Intake")
        master.geometry("400x500")
        master.configure(bg='#f0f4f8')

        # Title
        self.title_label = tk.Label(
            master, 
            text="Healthcare Patient Intake", 
            font=("Arial", 16, "bold"),
            bg='#f0f4f8',
            fg='#2c3e50'
        )
        self.title_label.pack(pady=20)

        # Name Input
        tk.Label(master, text="Patient Name", bg='#f0f4f8').pack()
        self.name_entry = tk.Entry(master, width=30)
        self.name_entry.pack(pady=10)

        # Age Input
        tk.Label(master, text="Patient Age", bg='#f0f4f8').pack()
        self.age_entry = tk.Entry(master, width=30)
        self.age_entry.pack(pady=10)

        # File Upload
        self.file_path = None
        self.file_button = tk.Button(
            master, 
            text="Upload Medical Document", 
            command=self.upload_file,
            bg='#3498db',
            fg='white'
        )
        self.file_button.pack(pady=10)

        self.file_label = tk.Label(master, text="No file selected", bg='#f0f4f8')
        self.file_label.pack(pady=5)

        # Submit Button
        self.submit_button = tk.Button(
            master, 
            text="Submit Patient Information", 
            command=self.submit_data,
            bg='#2ecc71',
            fg='white'
        )
        self.submit_button.pack(pady=20)

        # View Records Button
        self.view_button = tk.Button(
            master, 
            text="View Patient Records", 
            command=self.view_records,
            bg='#f39c12',
            fg='white'
        )
        self.view_button.pack(pady=20)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select Medical Document",
            filetypes=[("PDF files", "*.pdf"), ("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if self.file_path:
            self.file_label.config(text=os.path.basename(self.file_path))

    def submit_data(self):
        name = self.name_entry.get()
        age = self.age_entry.get()

        # Basic validation
        if not name or not age or not self.file_path:
            messagebox.showerror("Error", "Please fill in all fields and upload a file")
            return

        try:
            age = int(age)
            if age < 0 or age > 120:
                raise ValueError("Invalid age")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age")
            return

        # Import PatientDataManager inside the function to avoid circular import
        from patient_data_manager import PatientDataManager
        data_manager = PatientDataManager()
        data_manager.store_patient_data(name, age, self.file_path)

        # Simulate data submission (replace with actual backend processing)
        submission_info = f"Name: {name}\nAge: {age}\nFile: {self.file_path}"
        messagebox.showinfo("Submission Successful", submission_info)

        # Reset form
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.file_path = None
        self.file_label.config(text="No file selected")

    def view_records(self):
        # Import PatientDataManager to retrieve patient records
        from patient_data_manager import PatientDataManager
        data_manager = PatientDataManager()

        # Retrieve patient records
        records = data_manager.retrieve_patient_records()

        # Create a new window to display the records
        records_window = tk.Toplevel(self.master)
        records_window.title("Patient Records")
        records_window.geometry("500x400")

        # Create a listbox to display the records
        records_listbox = tk.Listbox(records_window, width=80, height=20)
        records_listbox.pack(pady=20)

        # Populate the listbox with records
        for record in records:
            record_text = f"Name: {record[1]}, Age: {record[2]}, File: {record[3]}"
            records_listbox.insert(tk.END, record_text)

def main():
    root = tk.Tk()
    dashboard = HealthcareDashboard(root)
    root.mainloop()

if __name__ == "__main__":
    main()
