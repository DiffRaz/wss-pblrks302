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
    session.clear()  # Clear session sebelum login
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validasi input username dan password
        if not username or not password:
            flash('Username and password are required!', 'error')
            return redirect(url_for('halamanlogin'))

        # Hash the password using md5 for comparison
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        cursor = None  # Inisialisasi awal untuk cursor
        try:
            # Buka koneksi baru untuk login
            cursor = db.cursor(dictionary=True)

            # Query untuk mencocokkan username dan password
            cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, hashed_password))
            user = cursor.fetchone()  # Mengambil satu baris data pengguna

            if user:
                # Simpan data pengguna dalam session
                session['username'] = user[0]['username']
                session['userType'] = user[0]['level']  # Ambil level pengguna dari kolom 'level' di database
                session['user_data'] = user

                # Redirect sesuai dengan level pengguna
                if user[0]['level'] == 'manager':
                    flash('Login successful! Welcome, Manager.', 'success')
                    return redirect(url_for('manager'))  # Halaman untuk level manager
                elif user[0]['level'] == 'staff':
                    flash('Login successful! Welcome, Staff.', 'success')
                    return redirect(url_for('staff'))  # Halaman untuk level staff
                else:
                    flash('User level not recognized.', 'error')
                    return redirect(url_for('halamanlogin'))
            else:
                flash('Invalid username or password!', 'error')

        except mysql.connector.Error as err:
            flash(f"Database error: {err}", 'error')

        finally:
            # Tutup cursor jika sudah diinisialisasi
            if cursor is not None:
                cursor.close()
            db.close()  # Tutup koneksi database

    return redirect(url_for('halamanlogin'))  # Jika metode selain POST, kembali ke halaman login
