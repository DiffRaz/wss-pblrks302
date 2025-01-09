from flask import request, redirect, url_for, flash, session
import mysql.connector


# Koneksi ke database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='pbl302'
    )

def list_data_sementara():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT * FROM list_barang_sementara"
        cursor.execute(query)
        data_barang = cursor.fetchall()
        return data_barang
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()