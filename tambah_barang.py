from flask import request, redirect, url_for, flash, session
import mysql.connector
import html
import random
import datetime
import string

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='pbl302'
)

def tambah_brg():
    if request.method == 'POST':
        nama_kilen = html.escape(request.form.get('nama_klien'))
        nama_barang = html.escape(request.form.get('nama_barang'))
        waktu_keluar = html.escape(request.form.get('date'))

        # Validasi input
        if not nama_kilen or not nama_barang or not waktu_keluar:
            flash('Semua input harus diisi.')
            return redirect(url_for('tambah_barangg'))

        panjang_kode = random.randint(8, 10)
        karakter = string.ascii_letters + string.digits
        kode_barang = ''.join(random.choice(karakter) for _ in range(panjang_kode))

        waktu_masuk = datetime.datetime.now().strftime("%Y-%m-%d")

        Status = "Belum diterima"

        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute(
                "INSERT INTO list_barang_sementara (nama_klien, nama_barang, kode_barang, waktu_masuk, waktu_keluar, status) VALUES (%s, %s, %s, %s, %s, %s)", 
                (nama_kilen, nama_barang, kode_barang, waktu_masuk, waktu_keluar, Status)
            )
            db.commit()  # Simpan perubahan ke database
            return redirect(url_for('tambah_barangg'))  # Redirect ke list_barang_staff setelah menambah barang
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            flash('Data tidak dapat disimpan. Silakan coba lagi.')
        finally:
            cursor.close()

    return redirect(url_for('halamanlogin'))