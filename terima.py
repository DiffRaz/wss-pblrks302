from flask import request, redirect, url_for, flash, session
import mysql.connector



def asep(id):
    try:
        db = mysql.connector.connect(host='localhost', user='manager', password='Gc.DGPYv44K)5Zb]', database='pbl302')
        cursor = db.cursor()

        # Pindahkan data dari tabel sementara ke tabel utama
        cursor.execute("""
            INSERT INTO list_barang (nama_klien, nama_barang, kode_barang, waktu_masuk, waktu_keluar)
            SELECT nama_klien, nama_barang, kode_barang, waktu_masuk, waktu_keluar
            FROM list_barang_sementara WHERE id = %s
        """, (id,))

        # Hapus data dari tabel sementara
        cursor.execute("UPDATE list_barang_sementara SET status = 'Sudah diterima' WHERE id = %s", (id,))

        db.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()