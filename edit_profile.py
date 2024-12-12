from flask import request, redirect, url_for, flash, session
import mysql.connector
import html
from time import sleep
import hashlib



# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='login',
    password='2c8b5C]Z*Na1o*VQ',
    database='pbl302'
)

def edit_profil():
    if request.method == 'POST':
        iduser = request.form.get('id')
        email = request.form.get('email')
        password = request.form.get('password')
        date = request.form.get('date')

        print(password)

        # Validasi input
        if not email or not password or not date :
            return redirect(url_for('edit_profil'))
        
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

            cursor.execute(
                "UPDATE login SET email = %s, password = %s, date = %s WHERE id = %s", 
                (email, hashed_password, date, iduser)
            )
            db.commit()  # Simpan perubahan ke database
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            db.close()  # Tutup koneksi setelah operasi
    sleep(2)
    return redirect(url_for('edit_profil'))
