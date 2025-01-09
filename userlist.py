import mysql.connector

def initiate_mysql_login_user_conn():
    return mysql.connector.connect(
    host='localhost',
    user='login',
    password='2c8b5C]Z*Na1o*VQ',
    database='pbl302'
)

def total_user_list_data():
    try:
        db = initiate_mysql_login_user_conn()
        cursor = db.cursor()
        count_query = "SELECT COUNT(*) FROM pbl302.login"
        cursor.execute(count_query)
        total_data = cursor.fetchall()[0][0]
        return total_data
    finally:
        cursor.close()
        db.close()

def return_user_list():
    db = initiate_mysql_login_user_conn()
    cursor = db.cursor(dictionary=True)
    query = f"SELECT id, username, email, date, level FROM pbl302.login"
    try:
        cursor.execute(query)
        user_list_dict = cursor.fetchall()
        return user_list_dict
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()

def remove_selected_user(id):
    try:
        db = initiate_mysql_login_user_conn()
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM pbl302.login WHERE id = {id}")
        db.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        return False
    finally:
        cursor.close()
        db.close()

def tampil_profile(id):
    db = initiate_mysql_login_user_conn()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM pbl302.login WHERE id = %s"
    try:
        cursor.execute(query, (id,))
        user_list_dict = cursor.fetchall()
        return user_list_dict
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()