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
        user_type = request.form.get('userType')

        if not username or not password or not user_type:
            flash('Username, password, and user type are required!')
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

            cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s AND level = %s", (username, hashed_password, user_type))
            user = cursor.fetchall()

            if user:
                session['username'] = username
                session['userType'] = user_type
                session['user_data'] = user
                if user_type == 'manager':
                    return redirect(url_for('manager'))
                elif user_type == 'staff':
                    return redirect(url_for('staff'))
            else:
                flash('Invalid username or password')

        finally:
            cursor.close()
            db.close()  # Tutup koneksi setelah operasi
    return redirect(url_for('halamanlogin'))

