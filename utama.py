import streamlit as st
import nosurat
import RegistArsipOut
import RegistArsipIn
import laporan
import sqlite3
from streamlit_option_menu import option_menu

# Fungsi untuk logout
def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""

def halaman_utama():
  with st.sidebar:
    selected = option_menu(
      menu_title="Main Menu",
      options=["Home", "Nomor Surat", "Upload Arsip", "Entri Arsip", "Laporan Daftar Arsip", "Klasifikasi dan JRA", "Contact", "Logout"],
      icons=["house", "book", "folder", "file-earmark-text", "archive", "calendar-days", "envelope", "box-arrow-right"],
      menu_icon="cast",
      default_index=0,
      styles={
        "container": {"padding": "0!important", "background-color": None},
        "icon": {"color": "orange", "font-size": "20px"},
        "nav-link": {
          "font-size": "16px",
          "text-align": "left",
          "margin" : "0px",
          "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "green"},
      },
    )

  if selected == "Nomor Surat":
    sub_selected = option_menu(
      menu_title="Nomor Surat",  # Title tidak ditampilkan di sidebar (kosongkan jika diinginkan)
      options=["View", "Edit", "Add"],  # Submenu options untuk Nomor Surat
      icons=["eye", "pencil", "plus-circle"],  # Ikon untuk submenu
      menu_icon="book",  # Ikon untuk submenu utama "Nomor Surat"
      default_index=0,  # Submenu default
      orientation="horizontal",  # Submenu ditampilkan secara horizontal
    )

    # Aksi untuk submenu "View", "Edit", dan "Add"
    if sub_selected == "View":
      nosurat.show_table()
    elif sub_selected == "Edit":
      nosurat.edit_nomor()
    elif sub_selected == "Add":
      nosurat.add_nomor()

  if selected == "Upload Arsip":
    sub_selected = option_menu(
      menu_title="Upload Arsip Masuk/Keluar",  # Title tidak ditampilkan di sidebar (kosongkan jika diinginkan)
      options=["Arsip Keluar", "Arsip Masuk"],  # Submenu options
      icons=["arrow-up", "arrow-down"],  # Ikon untuk submenu
      menu_icon="cloud-upload",  # Ikon untuk folder
      default_index=0,  # Default submenu
      orientation="horizontal",  # Menu secara horizontal di halaman utama
    )

    # Aksi untuk submenu "Arsip Keluar" dan "Arsip Masuk"
    if sub_selected == "Arsip Keluar":
      RegistArsipOut.utama_upload()
    elif sub_selected == "Arsip Masuk":
      RegistArsipIn.utama_uploadIn()

  if selected == "Entri Arsip":
    sub_selected = option_menu(
      menu_title="Entri Arsip Masuk/Keluar",  # Title tidak ditampilkan di sidebar (kosongkan jika diinginkan)
      options=["Arsip Keluar", "Arsip Masuk"],  # Submenu options
      icons=["arrow-up", "arrow-down"],  # Ikon untuk submenu
      menu_icon="pencil-square",  # Ikon untuk submenu utama
      default_index=0,  # Default submenu
      orientation="horizontal",  # Menu secara horizontal di halaman utama
    )
    # Aksi untuk submenu "Arsip Keluar" dan "Arsip Masuk"
    if sub_selected == "Arsip Keluar":
      RegistArsipOut.entri_arsip_keluar()
    elif sub_selected == "Arsip Masuk":
      RegistArsipIn.entri_manual()

  if selected == "Laporan Daftar Arsip":
    sub_selected = option_menu(
      menu_title="Laporan Daftar Arsip",  # Title tidak ditampilkan di sidebar (kosongkan jika diinginkan)
      options=["Arsip Aktif", "Arsip Inaktif", "Arsip Musnah", "Arsip Statis"],  # Submenu options
      icons=["file-earmark-check", "file-earmark-minus", "trash", "file-earmark-lock"],  # Ikon untuk submenu
      menu_icon="bar-chart",  # Ikon untuk submenu utama
      default_index=0,  # Default submenu
      orientation="horizontal",  # Menu secara horizontal di halaman utama
    )

    # Aksi untuk submenu "Daftar Arsip"
    if sub_selected == "Arsip Aktif":      
      laporan.lap_aktif()

    elif sub_selected == "Arsip Inaktif":
      laporan.lap_inaktif()
      
    elif sub_selected == "Arsip Musnah":
      laporan.lap_musnah()

    elif sub_selected == "Arsip Statis":
      laporan.lap_statis()
  if selected == "Klasifikasi dan JRA":
      st.write("Under Construction")
      
  else:
    if selected=="Home":
      
      #st.markdown("<h1 style='text-align: center;'>Sitem Informasi Manajemen Arsip</h1>", unsafe_allow_html=True)
      #st.markdown("<h1 style='text-align: center;'>(SIMARSIP)</h1>", unsafe_allow_html=True)
      #st.markdown("<h1 style='text-align: center;'>st.session_state['username']</h1>", unsafe_allow_html=True)

      col1, col2 = st.columns([1, 4])

      with col1:
          # Menampilkan logo sistem
          st.image("icon_siarsip.jpg", width=150)  # Ganti 'logo.png' dengan path logo Anda

      with col2:
        st.markdown("""
        ## Sistem Informasi Manajemen Arsip (SIMARSIP)
        """)

      # Deskripsi sistem
      st.markdown("""
      **SIMARSIP** adalah platform digital untuk mengelola, mencari, dan menyimpan arsip dengan mudah dan efisien. Dengan antarmuka yang sederhana dan fitur-fitur canggih, Anda dapat melakukan pencarian arsip, pengarsipan digital, dan akses arsip di mana saja dan kapan saja.
          
      ### Fitur Utama:
      - Registrasi Nomor Surat Keluar
      - Pengarsipan otomatis (Upload Arsip) dan manual (Entri Arsip)
      - Otomatisasi Pemberkasan Arsip sesuai kode klasifikasi
      - Pencarian berdasarkan metadata arsip
      - Laporan Daftar Arsip (Aktif, Inaktif, Musnah, Statis)
      - Statistik arsip
          
      Gunakan sistem ini untuk meningkatkan efisiensi dalam pengelolaan arsip kantor Anda.
      """)

      # Menambahkan tombol untuk tindakan
      #if st.button("Mulai Arsipkan"):
      #    st.write("Navigasi ke halaman arsip...")  # Fungsi ini dapat diarahkan ke halaman lain

      # Footer dengan icon dan informasi tambahan
      st.markdown("---")
      st.markdown("""
      <div style="text-align: center;">
          Copyright &copy; <b>Fathurrohman</b> - 2024
      </div>
      """, unsafe_allow_html=True)

    if selected =="Contact":
      st.title(f"Sub Menu Contact")
    if selected =="Logout":
      logout()

  return

#if __name__ == "__main__":
#    halaman_utama()
