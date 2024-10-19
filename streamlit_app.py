import streamlit as st
import create_db
import sqlite3
from utama import halaman_utama


# Fungsi untuk autentikasi pengguna
def authenticate(username, password, unit_id):
  conn = sqlite3.connect('simarsip.db')
  cursor = conn.cursor()
  cursor.execute("SELECT id, namauser, passw FROM pengguna WHERE namauser=? AND passw=? AND UnitKerja_id=?", (username, password, unit_id))
  user = cursor.fetchone()
  conn.close()
  return user

def auth_unit(id):
  conn = sqlite3.connect('simarsip.db')
  cursor = conn.cursor()
  cursor.execute("SELECT id, NamaUnit FROM UnitKerja WHERE id=?", (id,))
  unit = cursor.fetchone()
  conn.close()
  return unit 

def get_unit():
    conn = sqlite3.connect('simarsip.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, NamaUnit FROM UnitKerja")
    units = cursor.fetchall()
    #unitname = [row[0] for row in cursor.fetchall()]  # Mengambil semua username
    conn.close()
    return units

# Fungsi untuk logout
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""

# Fungsi untuk login
def login(user, idunit):
    st.session_state['logged_in'] = True
    st.session_state['id'] = user[0]
    st.session_state['namauser'] = user[1]
    st.session_state['Unit_id'] = idunit[0]
    st.session_state['NamaUnit'] = idunit[1]


# Halaman utama setelah login
def show_homepage():
    st.title(f"Selamat datang, {st.session_state['username']}!")
    st.write("Ini adalah halaman utama.")
    if st.button("Logout"):
        logout()

# Halaman login
def show_login_page():
    st.title("Halaman Login")
    daftar_unit = get_unit()

    # Membuat dropdown dengan NamaUnit dan menyimpan IdUnit yang dipilih
    #unit_names = [f"{unit[0]} ({unit[1]})" for unit in daftar_unit]  # Menampilkan NamaUnit dan IdUnit dalam dropdown
    unit_names = [f"{unit[1]}" for unit in daftar_unit] 
    selected_unit = st.selectbox("Unit Kerja", unit_names)

    # Mendapatkan id dari Unit yang dipilih
    username = st.text_input("Nama Pengguna")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        unit_id = [unit[0] for unit in daftar_unit if f"{unit[1]}" == selected_unit][0]
        user = authenticate(username, password, unit_id)
        #unit_id = [unit[0] for unit in daftar_unit if f"{unit[0]} ({unit[1]})" == selected_unit][0]
        if user:
            idunit = auth_unit(unit_id)
            #st.success("Login berhasil!")
            login(user, idunit)
        else:
            st.error("Username atau password salah!")

# Main logic
create_db.buat_db()
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.session_state['id'] = None

if st.session_state['logged_in']:
  halaman_utama()
else:
  show_login_page()
