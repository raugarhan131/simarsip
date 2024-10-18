import sqlite3
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder
import datetime

# Fungsi untuk menghubungkan dan membaca data dari database SQLite
def fetch_data_from_db(query):
    conn = sqlite3.connect('simarsip.db')  # Ganti dengan nama database kamu
    df = pd.read_sql(query, conn)  # Menjalankan query dan menyimpan hasil ke DataFrame
    conn.close()  # Menutup koneksi setelah membaca data
    return df

# Fungsi untuk memasukkan data ke tabel
def insert_data(unit_id, pengguna_id, nama_pengguna, tahun, no, hal, ka, no_surat, status, tglsurat):
    try:
        conn = sqlite3.connect('simarsip.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO NoSurat (UnitKerja_id, Pengguna_id, Nama_Pengguna, Tahun, No, Hal, KA, No_Surat, Status, TglSurat) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (unit_id, pengguna_id, nama_pengguna, tahun, no, hal, ka, no_surat, status, tglsurat))
        conn.commit()
        st.success("Data berhasil ditambahkan!")
    except sqlite3.Error as e:
        st.error(f"Error saat menyimpan data: {e}")
    finally:
        conn.close()

# Fungsi untuk memperbarui data yang sudah ada
def update_data(id, unit_kerja, pengguna_id, nama_pengguna, tahun, no, hal, ka, no_surat, status, tglsurat):
    try:
        conn = sqlite3.connect('simarsip.db')
        c = conn.cursor()
        c.execute('''
            UPDATE NoSurat 
            SET UnitKerja_id=?, Pengguna_id=?, Nama_Pengguna=?, Tahun=?, No=?, Hal=?, KA=?, No_Surat=?, Status=?, TglSurat=? 
            WHERE no=?
        ''', (unit_kerja, pengguna_id, nama_pengguna, tahun, no, hal, ka, no_surat, status, tglsurat, no))
        conn.commit()
        st.success("Data berhasil diperbaharui!")
    except sqlite3.Error as e:
        st.error(f"Error saat menyimpan data: {e}")
    finally:
        conn.close()

# Fungsi untuk menampilkan data dari tabel
def display_data():
    conn = sqlite3.connect('simarsip.db')
    c = conn.cursor()
    c.execute('SELECT * FROM NoSurat')
    rows = c.fetchall()
    conn.close()
    return rows

def get_nosurat():
    conn = sqlite3.connect('simarsip.db')
    c = conn.cursor()
    c.execute('SELECT * FROM NoSurat order by no desc')
    rows = c.fetchone()
    conn.close()
    return rows

def cek_nomor(no):
    conn = sqlite3.connect('simarsip.db')
    c = conn.cursor()
    c.execute('SELECT * FROM NoSurat where no=?', (no,))
    rows = c.fetchone()
    conn.close()
    return rows

# Fungsi untuk mendapatkan data berdasarkan ID
def get_data_by_id(id):
    conn = sqlite3.connect('simarsip.db')
    c = conn.cursor()
    c.execute('SELECT * FROM NoSurat WHERE no=?', (id,))
    row = c.fetchone()
    conn.close()
    return row


# Fungsi utama untuk menampilkan data
def show_table():
    query = "SELECT TglSurat, No_Surat, KA as [Kode Surat], Hal, Lokasi, Nama_Pengguna FROM NoSurat"  # Ganti dengan nama tabel yang diinginkan
        
    # Panggil fungsi untuk mengambil data dari database
    data = fetch_data_from_db(query)

    if not data.empty:
        st.subheader("Data Nomor Surat")
            
        # Mengkonfigurasi opsi untuk AgGrid
        gb = GridOptionsBuilder.from_dataframe(data)
        gb.configure_pagination(paginationAutoPageSize=True)  # Menambahkan pagination otomatis
        gb.configure_side_bar()  # Mengaktifkan sidebar filter di grid
        grid_options = gb.build()

        # Menampilkan data di AgGrid
        AgGrid(data, gridOptions=grid_options, enable_enterprise_modules=True)
    else:
        st.warning("Tidak ada data yang ditemukan dalam tabel.")

    return 

def edit_nomor():
    data = display_data()  # Ambil data yang ada
    if data:
        selected_id = st.selectbox("Pilih Data Nomor Surat yang akan diedit:", [row[6] for row in data])
        if selected_id:
            selected_data = get_data_by_id(selected_id)
            with st.form("edit_form"):
                unit_id = st.session_state['Unit_id']
                pengguna_id =  st.session_state['id']
                nama_pengguna = st.session_state['namauser']
                strtglsurat = st.date_input(
                "Tgl Surat", 
                    value=datetime.datetime.strptime(selected_data[4], "%d/%b/%Y").date() if selected_data else datetime.date.today()
                )
                no = st.number_input("Nomor", value=selected_data[6])
                hal = st.text_input("Hal", value=selected_data[7])
                ka = st.text_input("KA", value=selected_data[8])

                submitedit = st.form_submit_button("Simpan Data")

            if submitedit:
                tahun = strtglsurat.year
                tglsurat = strtglsurat.strftime("%d/%b/%Y")
                no_surat = f"{no}/IT3.D3/{ka}/M/B/{tahun}"
                status=0
                update_data(selected_id, unit_id, pengguna_id, nama_pengguna, tahun, no, hal, ka, no_surat, status, tglsurat)

def add_nomor(): 
    selected_data = None
    noakhir = get_nosurat()
    if noakhir:
        no = noakhir[6]+1
    else:
        no = 1
    status=0
    with st.form("input_form"):
        #unit_kerja = st.number_input("Unit Kerja ID", min_value=1, step=1, format="%d")
        hal = st.text_input("Perihal Surat")
        ka = st.text_input("Kode Surat")
        strtglsurat = st.date_input("Tanggal Surat", value=datetime.date.today())
        tahun = strtglsurat.year
        no_surat = f"{no}/IT3.D3/{ka}/M/B/{tahun}"
        tglsurat = strtglsurat.strftime("%d/%b/%Y")
        unit_id = st.session_state['Unit_id']
        pengguna_id =  st.session_state['id']
        nama_pengguna = st.session_state['namauser']
        submitadd = st.form_submit_button("Simpan Data")        

    if submitadd:
        if cek_nomor(no):
            st.error("Nomor Surat Sudah Ada !")
        else:
            insert_data(unit_id, pengguna_id, nama_pengguna, tahun, no, hal, ka, no_surat, status, tglsurat)
            #if not (unit_kerja and pengguna_id and nama_pengguna and hal and ka):
            #    st.error("Semua field harus diisi!")

def utama():
    tab1, tab2, tab3 = st.tabs(['View', 'Edit', "Add"])
    with tab1:
        show_table()
    with tab2:
        edit_nomor()
    with tab3:
        add_nomor()

"""
def entri_edit(mode):
    #show_table()
    # Pilihan untuk Add atau Edit
    #mode = st.radio("Pilih Mode:", ['Add', 'Edit'])
    selected_id = None
    selected_data = None

    if mode=="Edit":
        data = display_data()  # Ambil data yang ada
        if data:
            selected_id = st.selectbox("Pilih Data Nomor Surat yang akan diedit:", [row[6] for row in data])
        if selected_id:
            selected_data = get_data_by_id(selected_id)
            with st.form("input_form"):
                unit_kerja = st.number_input("Unit Kerja ID", value=selected_data[1])
                pengguna_id = st.number_input("Pengguna ID", value=selected_data[2])
                nama_pengguna = st.text_input("Nama Pengguna", value=selected_data[3])
                tglsurat = st.date_input(
                    "Tgl Surat", 
                    value=datetime.datetime.strptime(selected_data[4], "%Y-%m-%d").date() if selected_data else datetime.date.today()
                )
                no = st.number_input("Nomor", value=selected_data[6])
                hal = st.text_input("Hal", value=selected_data[7])
                ka = st.text_input("KA", value=selected_data[8])

                tahun = tglsurat.year
                no_surat = f"{no}/IT3/{ka}/M/B/{tahun}"
                status=0
                submit = st.form_submit_button("Simpan Data")

    if mode == "Add":
        selected_data = None
        noakhir = get_nosurat()
        no = noakhir[6]+1
        status=0
        with st.form("input_form"):
            unit_kerja = st.number_input("Unit Kerja ID", min_value=1, step=1, format="%d")
            pengguna_id = st.number_input("Pengguna ID", min_value=1, step=1, format="%d")
            nama_pengguna = st.text_input("Nama Pengguna")
            no = st.number_input("Nomor", value=no, min_value=no, step=0, format="%d")
            hal = st.text_input("Perihal Surat")
            ka = st.text_input("Kode Surat")
            tglsurat = st.date_input(
                "Tgl Surat", 
                value=datetime.datetime.strptime(datetime.date.today(), "%Y-%m-%d").date() if selected_data else datetime.date.today()
            )
            tahun = tglsurat.year
            no_surat = f"{no}/IT3/{ka}/M/B/{tahun}"
            submit = st.form_submit_button("Simpan Data")        

    # Jika tombol disubmit, tambahkan atau perbarui data
    if submit and mode=="Add":
        insert_data(unit_kerja, pengguna_id, nama_pengguna, tahun, no, hal, ka, no_surat, status, tglsurat)
        st.success("Data berhasil ditambahkan!")
    elif submit and mode=="Edit" and selected_id:
        update_data(selected_id, unit_kerja, pengguna_id, nama_pengguna, tahun, no, hal, ka, no_surat, status, tglsurat)
        st.success("Data berhasil diperbarui!")    



      unit_kerja = st.number_input("Unit Kerja ID", value=selected_data[1] if selected_data else 1)
      pengguna_id = st.number_input("Pengguna ID", value=selected_data[2] if selected_data else 1)
      nama_pengguna = st.text_input("Nama Pengguna", value=selected_data[3] if selected_data else "admin")
      tahun = st.text_input("Tahun", value=selected_data[4] if selected_data else "2024")
      no = st.number_input("Nomor", value=selected_data[5] if selected_data else 1)
      hal = st.text_input("Hal", value=selected_data[6] if selected_data else "Undangan")
      ka = st.text_input("KA", value=selected_data[7] if selected_data else "KM.05.00")
      no_surat = st.text_input("Nomor Surat", value=selected_data[8] if selected_data else "123/IT3.D3/KM.05.00/M/B/2024")
      status = st.selectbox("Status", [0, 1], index=selected_data[9] if selected_data else 1)

"""