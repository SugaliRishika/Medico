from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Create directory to store files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Store patient records (in-memory for simplicity)
patient_records = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_data():
    name = request.form.get('name')
    age = request.form.get('age')
    file = request.files.get('file')

    # Validate data
    if not name or not age or not file:
        flash("Please fill in all fields and upload a file.", "error")
        return redirect(url_for('index'))

    try:
        age = int(age)
        if age < 0 or age > 120:
            flash("Please enter a valid age.", "error")
            return redirect(url_for('index'))
    except ValueError:
        flash("Please enter a valid age.", "error")
        return redirect(url_for('index'))

    # Save file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Store patient data with an ID
    patient_id = len(patient_records) + 1
    patient_data = {'id': patient_id, 'name': name, 'age': age, 'file_path': file_path}
    patient_records.append(patient_data)

    flash("Patient information submitted successfully!", "success")
    return redirect(url_for('index'))


@app.route('/records')
def view_records():
    return render_template('records.html', records=patient_records)


@app.route('/edit/<int:patient_id>', methods=['GET', 'POST'])
def edit_record(patient_id):
    patient = next((p for p in patient_records if p['id'] == patient_id), None)
    if not patient:
        flash("Patient not found.", "error")
        return redirect(url_for('view_records'))

    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')

        try:
            age = int(age)
            if age < 0 or age > 120:
                flash("Please enter a valid age.", "error")
                return redirect(url_for('edit_record', patient_id=patient_id))
        except ValueError:
            flash("Please enter a valid age.", "error")
            return redirect(url_for('edit_record', patient_id=patient_id))

        patient['name'] = name
        patient['age'] = age

        flash("Patient information updated successfully!", "success")
        return redirect(url_for('view_records'))

    return render_template('edit_record.html', patient=patient)


@app.route('/delete/<int:patient_id>', methods=['POST'])
def delete_record(patient_id):
    global patient_records
    patient_records = [p for p in patient_records if p['id'] != patient_id]
    flash("Patient record deleted successfully!", "success")
    return redirect(url_for('view_records'))


if __name__ == '__main__':
    app.run(debug=True)
