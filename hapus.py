from flask import request, redirect, url_for, flash, session
import mysql.connector


def hapus(id):
    try:
        db = mysql.connector.connect(host='localhost', user='root', password='', database='pbl302')
        cursor = db.cursor()

        # Hapus data dari tabel sementara
        cursor.execute("DELETE FROM list_barang_sementara WHERE id = %s", (id,))

        db.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()