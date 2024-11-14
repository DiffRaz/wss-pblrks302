from flask import request, redirect, url_for, flash, session
import mysql.connector
import html
from time import sleep
import hashlib

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='manager',
    password='Gc.DGPYv44K)5Zb]',
    database='pbl302'
)

def tambah_usr():
    if request.method == 'POST':
        username = html.escape(request.form.get('username'))
        email = html.escape(request.form.get('email'))
        password = html.escape(request.form.get('password'))
        date = html.escape(request.form.get('date'))
        gender = html.escape(request.form.get('gendertype'))
        level = html.escape(request.form.get('level'))

        # Validasi input
        if not username or not email or not password or not date or not gender or not level:
            return redirect(url_for('add_user'))
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        try:
            # Buka koneksi baru
            db = mysql.connector.connect(
                host='localhost',
                user='manager',
                password='Gc.DGPYv44K)5Zb]',
                database='pbl302'
            )
            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "INSERT INTO login (username, email, password, date, gender, level) VALUES (%s, %s, %s, %s, %s, %s)", 
                (username, email, hashed_password, date, gender, level)
            )
            db.commit()  # Simpan perubahan ke database
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()  # Tutup koneksi setelah operasi
    sleep(2)
    return redirect(url_for('add_user'))
