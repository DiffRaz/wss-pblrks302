from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, render_template_string
import mysql.connector
import secrets
from login import login
from tambah_barang import tambah_brg
from tambah_user import tambah_usr
from list_barang_sementara import list_data_sementara
from terima import asep
from hapus import hapus
from list_barang_stok import list_barang_staff
from hapus2 import hapuus
from userlist import return_user_list, total_user_list_data, remove_selected_user, tampil_profile
from edit_profile import edit_profil
import hashlib

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Class untuk koneksi database
class DatabaseConnection:
    def __init__(self, user_type):
        self.user_type = user_type

    def get_connection(self):
        """membuka koneksi database berdasarkan jenis pengguna"""
        if self.user_type == "manager":
            return mysql.connector.connect(
                host='localhost',
                user='manager',
                password='Gc.DGPYv44K)5Zb]',
                database='pbl302'
            )
        elif self.user_type == "staff":
            return mysql.connector.connect(
                host='localhost',
                user='staff',
                password='P57L3P8_Sz4rR]TK',
                database='pbl302'
            )
        else:
            raise ValueError("User type tidak valid untuk koneksi database")

# Class untuk manajemen session pengguna
class UserSession:
    def __init__(self):
        self.user_data = session.get('user_data')
        self.user_type = session.get('userType')

    def is_authenticated(self):
        return self.user_data is not None

    def is_manager(self):
        return self.user_type == "manager"

    def is_staff(self):
        return self.user_type == "staff"

    def clear_session(self):
        session.clear()

# Class untuk operasi barang bagi manager
class BarangManager:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def list_barang(self):
        return list_data_sementara()

    def accept_barang(self, id_barang):
        return asep(id_barang)

    def hapus_barang(self, id_barang):
        return hapus(id_barang)

# Class untuk operasi barang bagi staff
class BarangStaff:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def list_barang(self):
        return list_barang_staff()

    def hapus_barang(self, id_barang):
        return hapuus(id_barang)

# Routes
@app.route('/')
def sign_in():
    UserSession().clear_session()
    return render_template("sign_in.html")

@app.route('/halamanlogin')
def halamanlogin():
    UserSession().clear_session()
    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    UserSession().clear_session()
    return login()

@app.route('/logout')
def logout():
    user_session = UserSession()
    if user_session.is_authenticated():
        user_data = user_session.user_data[0] if user_session.user_data else None
        session.clear()
    
    return redirect(url_for('halamanlogin'))

@app.route('/manager')
def manager():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_manager():
        user_data = user_session.user_data[0]
        return render_template(
            'dashboard2.html',
            username=user_data['username'],
            email=user_data['email'],
            gender=user_data['gender'],
            level=user_data['level'],
            iduser=user_data['id']

        )
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/staff')
def staff():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_staff():
        user_data = user_session.user_data[0]
        
        # Render email secara dinamis menggunakan render_template_string
        email_rendered = render_template_string(user_data['email'])
        
        return render_template(
            'dashboard1.html',
            username=user_data['username'],
            email=email_rendered,
            gender=user_data['gender'],
            level=user_data['level']
        )
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/list_barang/<int:page>')
def list_barang(page=1):
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_staff():
        db_conn = DatabaseConnection("staff")
        db = db_conn.get_connection()
        try:
            barang = BarangStaff(db)
            if page < 1:
                return redirect(url_for('list_barang', page=1))
        
            data_barang = barang.list_barang()
            
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM list_barang")
            total_data = cursor.fetchone()[0]
            cursor.close()

            # Jika tidak ada barang, arahkan ke halaman pertama dan tetap render list_barang.html
            if total_data == 0:
                return render_template('list_barang.html', username=user_session.user_data[0]['username'], data_barang=[], current_page=1, total_pages=1, start_number=0)


            return render_template(
                'list_barang.html',
                data_barang=data_barang,
                current_page=page,
                username=user_session.user_data[0]['username'],
                start_number=1
            )
        finally:
            db.close()
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/tambah_barang')
def tambah_barangg():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_staff():
        username = user_session.user_data[0]['username']
        return render_template('tambah_barang.html', username=username)
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/add_user')
def add_user():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_manager():
        username = user_session.user_data[0]['username']
        return render_template('add_user.html', username=username)
    else:
        return redirect(url_for('halamanlogin'))
    
@app.route('/userlist/<int:page>')
def user_list(page=1):
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_manager():
        username = user_session.user_data[0]['username']
        iduser = user_session.user_data[0]['id']
        total_list_user = total_user_list_data()
        user_list = return_user_list()
        if page < 1:
                return redirect(url_for('user_list', page=1))
        return render_template('user_list.html',username=username, iduser=iduser, current_page=page,users=user_list)
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/rm_usr', methods=["POST", "GET"])
def remove_user():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_manager():
        data = request.get_json()
        id_user = data.get('id')
        try:
            remove_selected_user(id_user)
            return jsonify({'status': 'success'}), 200
        except:
            return jsonify({'status': 'error'}), 500
    else:
        return redirect(url_for('halamanlogin'))


@app.route('/tambah_barang_aksi', methods=['GET', 'POST'])
def tambah_barang_route():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_staff():
        flash('Your item request has been submitted.<br><br><strong><em>Please wait for an approval from a manager.</em></strong>')
        return tambah_brg()  
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/tambah_user_aksi', methods=['GET', 'POST'])
def tambah_user_route():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_manager():
        return tambah_usr() 
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/list_barang_manager/<int:page>')
def list_barang_manager(page=1):
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_manager():
        db_conn = DatabaseConnection("manager")
        db = db_conn.get_connection()
        try:
            barang = BarangManager(db)
            if page < 1:
                return redirect(url_for('list_barang_manager', page=1))
            
            data_barang = barang.list_barang()

            cursor = db.cursor()
            cursor.execute("SELECT COUNT(*) FROM list_barang_sementara")
            total_data = cursor.fetchone()[0]
            cursor.close()

            # Jika tidak ada barang, arahkan ke halaman pertama dan tetap render list_barang_manager.html
            if total_data == 0:
                return render_template('list_barang_manager.html', username=user_session.user_data[0]['username'], data_barang=[], current_page=1, total_pages=1, start_number=0)

            return render_template(
                'list_barang_manager.html',
                data_barang=data_barang,
                current_page=page,
                username=user_session.user_data[0]['username'],
            )
        finally:
            db.close()
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/accept', methods=['POST', 'GET'])
def accept_barang():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_manager():
        data = request.get_json()
        id_barang = data.get('id')

        if BarangManager(DatabaseConnection("manager")).accept_barang(id_barang):
            flash('Barang berhasil diterima dan dipindahkan ke list barang utama.')
            return jsonify({'status': 'success'}), 200
        else:
            flash('Terjadi kesalahan saat memproses data.')
            return jsonify({'status': 'error'}), 500
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/hapus', methods=['POST', 'GET'])
def hapus_barang():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_manager():
        data = request.get_json()
        id_barang = data.get('id')

        if BarangManager(DatabaseConnection("manager")).hapus_barang(id_barang):
            flash('Barang berhasil dihapus.')
            return jsonify({'status': 'success'}), 200
        else:
            flash('Terjadi kesalahan saat memproses data.')
            return jsonify({'status': 'error'}), 500
    else:
        return redirect(url_for('halamanlogin'))

@app.route('/apus', methods=['POST', 'GET'])
def apus():
    user_session = UserSession()
    if user_session.is_authenticated() and user_session.is_staff():
        data = request.get_json()
        id_barang = data.get('id')

        if BarangStaff(DatabaseConnection("staff")).hapus_barang(id_barang):
            return jsonify({'status': 'success'}), 200
        else:
            flash('Terjadi kesalahan saat memproses data.')
            return jsonify({'status': 'error'}), 500
    else:
        return redirect(url_for('halamanlogin'))
    
@app.route('/edit_profil')
def edit_profil():
    user_session = UserSession()
    if user_session.is_authenticated():
        username = user_session.user_data[0]['username']
        iduser = user_session.user_data[0]['id']
        level = user_session.user_data[0]['level']
        profil = tampil_profile(iduser)
        if level == "manager" :
            return render_template('edit_profil2.html', username=username, profil=profil, idusr=iduser)
        else :
            return render_template('edit_profil.html', username=username, profil=profil, idusr=iduser)
    else:
        return redirect(url_for('halamanlogin'))
    
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile_route():
    user_session = UserSession()
    if not user_session.is_authenticated():
        return redirect(url_for('halamanlogin'))
    
    # Ambil data dari formulir
    user_id = user_session.user_data[0]['id']
    user_level = user_session.user_data[0]['level']
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm', '').strip()
    date = request.form.get('date', '').strip()

    # Validasi input kosong
    if not email or not password or not confirm or not date:
        flash('Semua kolom harus diisi.', 'error')
        return redirect(url_for('edit_profile_route'))

    # Validasi format email sederhana
    # import re
    # email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    # if not re.match(email_pattern, email):
    #     flash('Alamat email tidak valid.', 'error')
    #     return redirect(url_for('edit_profile_route'))
    
    # Validasi password dan confirm password
    if password != confirm:
        flash('Password dan konfirmasi tidak cocok.', 'error')
        return redirect(url_for('edit_profile_route'))
    
    # Enkripsi password
    hashed_password = hashlib.sha3_512(password.encode()).hexdigest()

    # Koneksi ke database
    db = mysql.connector.connect(
        host='localhost',
        user='login',
        password='2c8b5C]Z*Na1o*VQ',
        database='pbl302'
    )
    cursor = db.cursor(dictionary=True)

    # Update profil
    try:
        cursor.execute(
            "UPDATE login SET email=%s, password=%s, date=%s WHERE id=%s",
            (email, hashed_password, date, user_id)
        )
        db.commit()
        flash('Profil berhasil diperbarui.', 'success')
    except Exception as e:
        db.rollback()
        flash(f'Gagal memperbarui profil: {str(e)}', 'error')
    finally:
        cursor.close()
        db.close()

    return redirect(url_for(user_level))

if __name__ == '__main__':
    app.run(ssl_context=("wssprivatecert.crt", "wssprivate.key"), port=443, host='0.0.0.0')
