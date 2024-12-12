from flask import request, render_template, redirect, url_for, flash
import mysql.connector
import hashlib
import html

# Database connection function for adding a user
def tambah_usr():
    if request.method == 'POST':
        username = html.escape(request.form.get('username'))
        email = html.escape(request.form.get('email'))
        password = html.escape(request.form.get('password'))
        date = html.escape(request.form.get('date'))
        gender = html.escape(request.form.get('gendertype'))
        level = html.escape(request.form.get('level'))

        # Validasi input
        if not username or not email or not password or not date or not gender or not level:
            flash('All fields are required!', 'error')
            return redirect(url_for('add_user'))
        
        try:
            # Database connection using the 'login' user for the initial check
            db = mysql.connector.connect(
                host='localhost',
                user='login',  # Use 'login' user
                password='2c8b5C]Z*Na1o*VQ',  # Specified password
                database='pbl302'
            )

            cursor = db.cursor(dictionary=True)

            # Check if username exists
            cursor.execute("SELECT * FROM login WHERE username = %s", (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                # If username exists, send the flag to template to show SweetAlert
                return render_template('add_user.html', username_exists=True)

            # Switch to the 'manager' user for inserting the new user
            db.close()  # Close the current connection

            db = mysql.connector.connect(
                host='localhost',
                user='manager',  # Use 'manager' user for insertion
                password='Gc.DGPYv44K)5Zb]',  # Specified password
                database='pbl302'
            )

            cursor = db.cursor()

            # If username doesn't exist, proceed with inserting the new user
            hashed_password = hashlib.md5(password.encode()).hexdigest()

            cursor.execute(
                "INSERT INTO login (username, email, password, date, gender, level) VALUES (%s, %s, %s, %s, %s, %s)", 
                (username, email, hashed_password, date, gender, level)
            )
            db.commit()  # Save changes to the database
            if cursor.rowcount > 0:
                flash('User successfully added!', 'success')  # Menampilkan pesan sukses jika INSERT berhasil

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            flash('An error occurred while adding the user.', 'error')
        finally:
            cursor.close()

    return redirect(url_for('add_user'))
