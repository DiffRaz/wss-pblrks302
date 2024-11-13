import mysql.connector

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='login',
    password='2c8b5C]Z*Na1o*VQ',
    database='pbl302'
)

def total_user_list_data():
    try:
        cursor = db.cursor()
        count_query = "SELECT COUNT(*) FROM pbl302.login"
        cursor.execute(count_query)
        total_data = cursor.fetchone()[0]
        return total_data
    finally:
        cursor.close()

def return_user_list(limit, offset):
    cursor = db.cursor(dictionary=True)
    query = f"SELECT id, username, email, date, gender, level FROM pbl302.login LIMIT {limit} OFFSET {offset}"
    try:
        cursor.execute(query)
        user_list_dict = cursor.fetchall()
        return user_list_dict
    except mysql.connector.Error as e:
        print(f"Kesalahan Terjadi: {e}")
    finally:
        cursor.close()

def remove_selected_user(id):
    try:
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