from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_long_random_secret_key_here'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'aisha'
app.config['MYSQL_DB'] = 'sample'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # For dict-like rows

mysql = MySQL(app)

@app.route('/doctors')
def show_doctors():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT d.*, COUNT(DISTINCT p.AadharID) as PatientCount 
        FROM Doctor d 
        LEFT JOIN Patient p ON d.AadharID = p.PrimaryPhysicianID 
        GROUP BY d.AadharID, d.Name, d.Specialty, d.YearsOfExperience
    """)
    doctors = cur.fetchall()
    cur.close()
    return render_template('doctors.html', doctors=doctors)

@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        aadhar = request.form['aadhar']
        name = request.form['name']
        specialty = request.form['specialty']
        years = request.form['years']
        cur = mysql.connection.cursor()
        cur.callproc('add_doctor', (aadhar, name, specialty, int(years)))
        mysql.connection.commit()
        cur.close()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('show_doctors'))
    return render_template('add_doctor.html')

@app.route('/doctors/update/<aadhar>', methods=['GET', 'POST'])
def update_doctor(aadhar):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        specialty = request.form['specialty']
        years = request.form['years']
        cur.callproc('update_doctor', (aadhar, name, specialty, int(years)))
        mysql.connection.commit()
        cur.close()
        flash('Doctor updated!', 'success')
        return redirect(url_for('show_doctors'))
    cur.execute("SELECT * FROM Doctor WHERE AadharID = %s", (aadhar,))
    doctor = cur.fetchone()
    cur.close()
    return render_template('update_doctor.html', doctor=doctor)

@app.route('/doctors/delete/<aadhar>', methods=['POST'])
def delete_doctor(aadhar):
    cur = mysql.connection.cursor()
    try:
        cur.callproc('delete_doctor', (aadhar,))
        mysql.connection.commit()
        flash('Doctor deleted!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    cur.close()
    return redirect(url_for('show_doctors'))

@app.route('/patients')
def show_patients():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Patient")
    patients = cur.fetchall()
    cur.close()
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        aadhar = request.form['aadhar']
        name = request.form['name']
        address = request.form['address']
        birthdate = request.form['birthdate']
        physician = request.form['physician']
        cur = mysql.connection.cursor()
        cur.callproc('add_patient', (aadhar, name, address, birthdate, physician))
        mysql.connection.commit()
        cur.close()
        flash('Patient added successfully!', 'success')
        return redirect(url_for('show_patients'))
    return render_template('add_patient.html')

@app.route('/patients/update/<aadhar>', methods=['GET', 'POST'])
def update_patient(aadhar):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        birthdate = request.form['birthdate']
        physician = request.form['physician']
        cur.callproc('update_patient', (aadhar, name, address, birthdate, physician))
        mysql.connection.commit()
        cur.close()
        flash('Patient updated!', 'success')
        return redirect(url_for('show_patients'))
    cur.execute("SELECT * FROM Patient WHERE AadharID = %s", (aadhar,))
    patient = cur.fetchone()
    cur.close()
    return render_template('update_patient.html', patient=patient)

@app.route('/patients/delete/<aadhar>', methods=['POST'])
def delete_patient(aadhar):
    cur = mysql.connection.cursor()
    try:
        cur.callproc('delete_patient', (aadhar,))
        mysql.connection.commit()
        flash('Patient deleted!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    cur.close()
    return redirect(url_for('show_patients'))

@app.route('/pharma')
def show_pharma():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM PharmaceuticalCompany")
    companies = cur.fetchall()
    cur.close()
    return render_template('pharma.html', companies=companies)

@app.route('/pharma/add', methods=['GET', 'POST'])
def add_pharma():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.callproc('add_pharma_company', (name, phone))
        mysql.connection.commit()
        cur.close()
        flash('Pharmaceutical Company added successfully!', 'success')
        return redirect(url_for('show_pharma'))
    return render_template('add_pharma.html')

@app.route('/pharma/update/<name>', methods=['GET', 'POST'])
def update_pharma(name):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        phone = request.form['phone']
        cur.callproc('update_pharma_company', (name, phone))
        mysql.connection.commit()
        cur.close()
        flash('Pharmaceutical Company updated!', 'success')
        return redirect(url_for('show_pharma'))
    cur.execute("SELECT * FROM PharmaceuticalCompany WHERE Name = %s", (name,))
    company = cur.fetchone()
    cur.close()
    return render_template('update_pharma.html', company=company)

@app.route('/pharma/delete/<name>', methods=['POST'])
def delete_pharma(name):
    cur = mysql.connection.cursor()
    try:
        cur.callproc('delete_pharma_company', (name,))
        mysql.connection.commit()
        flash('Pharmaceutical Company deleted!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    cur.close()
    return redirect(url_for('show_pharma'))

@app.route('/drugs')
def show_drugs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Drug")
    drugs = cur.fetchall()
    cur.close()
    return render_template('drugs.html', drugs=drugs)

@app.route('/drugs/add', methods=['GET', 'POST'])
def add_drug():
    if request.method == 'POST':
        trade_name = request.form['trade_name']
        formula = request.form['formula']
        company_name = request.form['company_name']
        cur = mysql.connection.cursor()
        cur.callproc('add_drug', (trade_name, formula, company_name))
        mysql.connection.commit()
        cur.close()
        flash('Drug added successfully!', 'success')
        return redirect(url_for('show_drugs'))
    return render_template('add_drug.html')

@app.route('/drugs/update/<trade_name>/<company_name>', methods=['GET', 'POST'])
def update_drug(trade_name, company_name):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        formula = request.form['formula']
        cur.callproc('update_drug', (trade_name, company_name, formula))
        mysql.connection.commit()
        cur.close()
        flash('Drug updated!', 'success')
        return redirect(url_for('show_drugs'))
    cur.execute("SELECT * FROM Drug WHERE TradeName = %s AND CompanyName = %s", (trade_name, company_name))
    drug = cur.fetchone()
    cur.close()
    return render_template('update_drug.html', drug=drug)

@app.route('/drugs/delete/<trade_name>/<company_name>', methods=['POST'])
def delete_drug(trade_name, company_name):
    cur = mysql.connection.cursor()
    try:
        cur.callproc('delete_drug', (trade_name, company_name))
        mysql.connection.commit()
        flash('Drug deleted!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    cur.close()
    return redirect(url_for('show_drugs'))

@app.route('/pharmacies')
def show_pharmacies():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Pharmacy")
    pharmacies = cur.fetchall()
    cur.close()
    return render_template('pharmacies.html', pharmacies=pharmacies)

@app.route('/pharmacies/add', methods=['GET', 'POST'])
def add_pharmacy():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.callproc('add_pharmacy', (name, address, phone))
        mysql.connection.commit()
        cur.close()
        flash('Pharmacy added successfully!', 'success')
        return redirect(url_for('show_pharmacies'))
    return render_template('add_pharmacy.html')

@app.route('/pharmacies/update/<name>', methods=['GET', 'POST'])
def update_pharmacy(name):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        address = request.form['address']
        phone = request.form['phone']
        cur.callproc('update_pharmacy', (name, address, phone))
        mysql.connection.commit()
        cur.close()
        flash('Pharmacy updated!', 'success')
        return redirect(url_for('show_pharmacies'))
    cur.execute("SELECT * FROM Pharmacy WHERE Name = %s", (name,))
    pharmacy = cur.fetchone()
    cur.close()
    return render_template('update_pharmacy.html', pharmacy=pharmacy)

@app.route('/pharmacies/delete/<name>', methods=['POST'])
def delete_pharmacy(name):
    cur = mysql.connection.cursor()
    try:
        cur.callproc('delete_pharmacy', (name,))
        mysql.connection.commit()
        flash('Pharmacy deleted!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    cur.close()
    return redirect(url_for('show_pharmacies'))

@app.route('/sells')
def show_sells():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Sells")
    sells = cur.fetchall()
    cur.close()
    return render_template('sells.html', sells=sells)

@app.route('/sells/add', methods=['GET', 'POST'])
def add_sells():
    if request.method == 'POST':
        pharmacy = request.form['pharmacy']
        trade_name = request.form['trade_name']
        company_name = request.form['company_name']
        price = request.form['price']
        cur = mysql.connection.cursor()
        cur.callproc('add_sells', (pharmacy, trade_name, company_name, float(price)))
        mysql.connection.commit()
        cur.close()
        flash('Sells record added successfully!', 'success')
        return redirect(url_for('show_sells'))
    return render_template('add_sells.html')

@app.route('/sells/update/<pharmacy>/<trade_name>/<company_name>', methods=['GET', 'POST'])
def update_sells(pharmacy, trade_name, company_name):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        price = request.form['price']
        cur.callproc('update_sells', (pharmacy, trade_name, company_name, float(price)))
        mysql.connection.commit()
        cur.close()
        flash('Sells record updated!', 'success')
        return redirect(url_for('show_sells'))
    cur.execute("SELECT * FROM Sells WHERE PharmacyName = %s AND TradeName = %s AND CompanyName = %s", 
                (pharmacy, trade_name, company_name))
    sell = cur.fetchone()
    cur.close()
    return render_template('update_sells.html', sell=sell)

@app.route('/sells/delete/<pharmacy>/<trade_name>/<company_name>', methods=['POST'])
def delete_sells(pharmacy, trade_name, company_name):
    cur = mysql.connection.cursor()
    try:
        cur.callproc('delete_sells', (pharmacy, trade_name, company_name))
        mysql.connection.commit()
        flash('Sells record deleted!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    cur.close()
    return redirect(url_for('show_sells'))

@app.route('/prescriptions')
def show_prescriptions():
    cur = mysql.connection.cursor()
    cur.execute("SELECT p.*, pd.TradeName, pd.CompanyName, pd.Quantity FROM Prescription p LEFT JOIN PrescriptionDrug pd ON p.DoctorID = pd.DoctorID AND p.PatientID = pd.PatientID AND p.Date = pd.Date")
    prescriptions = cur.fetchall()
    cur.close()
    return render_template('prescriptions.html', prescriptions=prescriptions)

@app.route('/prescriptions/add', methods=['GET', 'POST'])
def add_prescription():
    if request.method == 'POST':
        doctor_id = request.form['doctor_id']
        patient_id = request.form['patient_id']
        date = request.form['date']
        trade_name = request.form.get('trade_name')
        company_name = request.form.get('company_name')
        quantity = request.form.get('quantity')

        cur = mysql.connection.cursor()
        if trade_name and company_name and quantity:
            cur.callproc('add_prescription_drug', (doctor_id, patient_id, date, trade_name, company_name, int(quantity)))
        else:
            cur.callproc('add_prescription', (doctor_id, patient_id, date))
        mysql.connection.commit()
        cur.close()
        flash('Prescription added successfully!', 'success')
        return redirect(url_for('show_prescriptions'))
    return render_template('add_prescription.html')

@app.route('/prescriptions/update/<doctor_id>/<patient_id>/<date>', methods=['GET', 'POST'])
def update_prescription(doctor_id, patient_id, date):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        new_date = request.form['date']
        cur.callproc('update_prescription_date', (doctor_id, patient_id, date, new_date))
        mysql.connection.commit()
        cur.close()
        flash('Prescription updated!', 'success')
        return redirect(url_for('show_prescriptions'))
    cur.execute("""
        SELECT p.*, pd.TradeName, pd.CompanyName, pd.Quantity 
        FROM Prescription p 
        LEFT JOIN PrescriptionDrug pd ON p.DoctorID = pd.DoctorID 
            AND p.PatientID = pd.PatientID 
            AND p.Date = pd.Date 
        WHERE p.DoctorID = %s AND p.PatientID = %s AND p.Date = %s
    """, (doctor_id, patient_id, date))
    prescription = cur.fetchone()
    cur.close()
    return render_template('update_prescription.html', prescription=prescription)

@app.route('/prescriptions/delete/<doctor_id>/<patient_id>/<date>', methods=['POST'])
def delete_prescription(doctor_id, patient_id, date):
    cur = mysql.connection.cursor()
    try:
        cur.callproc('delete_prescription', (doctor_id, patient_id, date))
        mysql.connection.commit()
        flash('Prescription deleted!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    cur.close()
    return redirect(url_for('show_prescriptions'))

@app.route('/contracts')
def show_contracts():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM Contract")
    contracts = cur.fetchall()
    cur.close()
    return render_template('contracts.html', contracts=contracts)

@app.route('/contracts/add', methods=['GET', 'POST'])
def add_contract():
    if request.method == 'POST':
        pharmacy = request.form['pharmacy']
        company = request.form['company']
        supervisor = request.form['supervisor']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        text = request.form['text']
        cur = mysql.connection.cursor()
        cur.callproc('add_contract', (pharmacy, company, supervisor, start_date, end_date, text))
        mysql.connection.commit()
        cur.close()
        flash('Contract added successfully!', 'success')
        return redirect(url_for('show_contracts'))
    return render_template('add_contract.html')

@app.route('/contracts/update/<pharmacy>/<company>', methods=['GET', 'POST'])
def update_contract(pharmacy, company):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        supervisor = request.form['supervisor']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        text = request.form['text']
        cur.callproc('update_contract', (pharmacy, company, supervisor, start_date, end_date, text))
        mysql.connection.commit()
        cur.close()
        flash('Contract updated!', 'success')
        return redirect(url_for('show_contracts'))
    cur.execute("SELECT * FROM Contract WHERE PharmacyName = %s AND CompanyName = %s", (pharmacy, company))
    contract = cur.fetchone()
    cur.close()
    return render_template('update_contract.html', contract=contract)

@app.route('/contracts/delete/<pharmacy>/<company>', methods=['POST'])
def delete_contract(pharmacy, company):
    cur = mysql.connection.cursor()
    try:
        cur.callproc('delete_contract', (pharmacy, company))
        mysql.connection.commit()
        flash('Contract deleted!', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    cur.close()
    return redirect(url_for('show_contracts'))

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT Name FROM Pharmacy")
    pharmacies = cur.fetchall()
    cur.execute("SELECT Name FROM PharmaceuticalCompany")
    companies = cur.fetchall()
    cur.close()
    return render_template('home.html', pharmacies=pharmacies, companies=companies)

@app.route('/reports/patient-prescriptions', methods=['GET', 'POST'])
def report_patient_prescriptions():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        
        cur = mysql.connection.cursor()
        cur.callproc('report_prescriptions_for_patient', (patient_id, start_date, end_date))
        prescriptions = cur.fetchall()
        cur.close()
        return render_template('report_prescriptions.html', prescriptions=prescriptions)
    return render_template('report_prescriptions_form.html')

@app.route('/reports/drugs-by-company/<company>')
def get_drugs_by_company(company):
    cur = mysql.connection.cursor()
    cur.callproc('get_drugs_by_company', (company,))
    drugs = cur.fetchall()
    cur.close()
    return render_template('company_drugs.html', drugs=drugs, company=company)

@app.route('/reports/pharmacy-stock/<pharmacy>')
def get_pharmacy_stock(pharmacy):
    cur = mysql.connection.cursor()
    cur.callproc('get_pharmacy_stock', (pharmacy,))
    stock = cur.fetchall()
    cur.close()
    return render_template('pharmacy_stock.html', stock=stock, pharmacy=pharmacy)

@app.route('/doctors/patients/<doctor_id>')
def get_doctor_patients(doctor_id):
    cur = mysql.connection.cursor()
    cur.callproc('get_patients_for_doctor', (doctor_id,))
    patients = cur.fetchall()
    cur.close()
    return render_template('doctor_patients.html', patients=patients, doctor_id=doctor_id)

if __name__ == '__main__':
    app.run(debug=True)
