from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from flask_session import Session  # Import Flask-Session
import datetime
import definations as df
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import mysql.connector
app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'your_secret_key'


# Configure Flask-Session to use Redis for session storage
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Aniket@9'
app.config['MYSQL_DB'] = 'kissdb'

mysql = mysql.connector.connect(host=app.config['MYSQL_HOST'], user=app.config['MYSQL_USER'],
                                password=app.config['MYSQL_PASSWORD'], database=app.config['MYSQL_DB'])

cursor = mysql.cursor()
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Flask-Session
# Session(app)

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        global usernumber
        usernumber = request.form['usernumber']
        password = request.form['password']
        
                    
        # Check if the usernumber and password match a record in the kissdb
        cursor.execute('SELECT * FROM users WHERE usernumber = %s', (usernumber,))
        # cursor.execute(query)
        user = cursor.fetchone()
        # cursor.close()
        if user and user[2] == password:  # Insecure, use hashing (as shown in previous answers)
            session['user_id'] = user[0]
            session['username'] = user[1]
            error_message = "Login Successfull!"
            return redirect(url_for('dashboard'))
        else:
            error_message = "Please enter correct password"
            return render_template('login.html',error_message=error_message)

    return render_template('login.html')

# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        usernumber = request.form['usernumber']
        password = request.form['password']
        uid=df.mydef.generate_user_id()
        ref_by=request.form['ref_code']
        current_time = datetime.now()

        # connection  = df.mydef.connect_mysql()
        # cursor_id = connection.cursor()

        # Check if the usernumber already exists in the kissdb
        query = f"SELECT * FROM users WHERE usernumber = '{usernumber}'"
        cursor.execute(query)
        existing_user = cursor.fetchone()

        if existing_user:
            flash('usernumber already exists. Please choose a different one.', 'danger')
        else:
            query = f"SELECT * FROM users WHERE uid = '{ref_by}'"
            cursor.execute(query)
            existing_ref_by = cursor.fetchone()
            if existing_ref_by:
                query = "INSERT INTO users (usernumber, password, uid, ref_by,register_date, name) VALUES (%s, %s, %s, %s, %s,%s)"
                cursor.execute(query, (usernumber, password, uid, ref_by,current_time, name))
                added_amount=0
                query = "INSERT INTO users_tdata (uid,added_amount,amt_added_date) VALUES (%s,%s,%s)"
                cursor.execute(query, (uid,added_amount,current_time))
                total_amt=0
                query = "INSERT INTO total_amount (uid,total_amt,updated_datetime) VALUES (%s,%s,%s)"
                cursor.execute(query, (uid,total_amt,current_time))
                query = "INSERT INTO withdrawal_transactions (uid,amount,date) VALUES (%s,%s,%s)"
                amount=0
                cursor.execute(query, (uid,amount,current_time))
                mysql.commit()
                # cursor.close()
                return redirect(url_for('login'))

    return render_template('register.html')
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        flash('You must be logged in to access the dashboard.', 'danger')
        return redirect(url_for('login'))



@app.route('/logout')
def logout():
    # Clear the user's session data
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
