from flask import request, redirect, url_for, flash, session
import mysql.connector


def hapuus(id):
    try:
        db = mysql.connector.connect(host='localhost', user='staff', password='P57L3P8_Sz4rR]TK', database='pbl302')
        cursor = db.cursor()

        # Hapus data dari tabel sementara
        cursor.execute("DELETE FROM list_barang WHERE id = %s", (id,))


        db.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()