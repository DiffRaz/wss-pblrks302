from flask import request, redirect, url_for, flash, session
import mysql.connector
import hashlib

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='login',
    password='2c8b5C]Z*Na1o*VQ',
    database='pbl302'
)

def login():
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        

        if not username or not password :
            flash('Username and password are required!', 'error')
            return redirect(url_for('halamanlogin'))

        # Hash the password using md5 for comparison
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        try:
            # Buka koneksi baru
            db = mysql.connector.connect(
                host='localhost',
                user='login',
                password='2c8b5C]Z*Na1o*VQ',
                database='pbl302'
            )
            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s ", (username, hashed_password))
            user = cursor.fetchall()

            if user:
                session['username'] = username
                session['userType'] = user[0]['level']
                session['user_data'] = user
                print(user[0]['level'])
                if user[0]['level'] == 'manager':
                    flash('Login successful! Welcome, Manager.', 'success')
                    return redirect(url_for('manager'))
                elif user[0]['level'] == 'staff':
                    flash('Login successful! Welcome, Staff.', 'success')
                    return redirect(url_for('staff'))
            else:
                flash('Invalid username or password!', 'error')

        finally:
            cursor.close()
            db.close()  # Tutup koneksi setelah operasi
    return redirect(url_for('halamanlogin'))