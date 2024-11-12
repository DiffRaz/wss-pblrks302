from flask import request, redirect, url_for, flash, session
import mysql.connector


# Koneksi ke database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='manager',
        password='Gc.DGPYv44K)5Zb]',
        database='pbl302'
    )

def list_data_sementara(limit, offset):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT * FROM list_barang_sementara LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
        data_barang = cursor.fetchall()
        return data_barang
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()