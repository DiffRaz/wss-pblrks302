from flask import request, redirect, url_for, flash, session
import mysql.connector


# Koneksi ke database
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='staff',
        password='P57L3P8_Sz4rR]TK',
        database='pbl302'
    )

def list_barang_staff():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        query = "SELECT * FROM list_barang"
        cursor.execute(query)
        data_barang = cursor.fetchall()
        return data_barang
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        db.close()