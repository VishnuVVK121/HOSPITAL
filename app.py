
from flask import Flask, render_template, request, redirect, flash, url_for
from db import Database

app = Flask(__name__)
app.secret_key = "super_secret_key"
db = Database()

@app.route('/')
def index():
    patients = db.get_all_patients()
    return render_template('index.html', patients=patients)

@app.route('/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        pid = request.form.get('id')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        illness = request.form.get('illness')

        if not all([pid, name, age, gender, illness]):
            flash("All fields are required.", "danger")
            return redirect(url_for('add_patient'))

        if db.get_patient(pid):
            flash("Patient ID already exists.", "warning")
            return redirect(url_for('add_patient'))

        db.add_patient(pid, name, int(age), gender, illness)
        flash("Patient added successfully.", "success")
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/search', methods=['GET', 'POST'])
def search_patient():
    patient = None
    if request.method == 'POST':
        pid = request.form.get('id')
        patient = db.get_patient(pid)
        if not patient:
            flash("Patient not found.", "danger")
    return render_template('search.html', patient=patient)

@app.route('/discharge/<string:pid>')
def discharge_patient(pid):
    if db.delete_patient(pid):
        flash("Patient discharged successfully.", "info")
    else:
        flash("Patient not found.", "danger")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
