import os
import streamlit as st

# Fungsi untuk membaca isi direktori
def list_directory(path):
    folders = []
    files = []
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                folders.append(item)
            else:
                files.append(item)
    except FileNotFoundError:
        st.error("Path tidak ditemukan.")
    return folders, files

def explor_arsip():
    # Mendapatkan path ke direktori sistem tempat aplikasi dijalankan
    base_directory = os.getcwd()  # Direktori saat ini (tempat aplikasi dijalankan)
    berkas_path = os.path.join(base_directory, "berkas")  # Menambahkan subfolder "berkas"

    # Membuat folder "berkas" jika belum ada
    if not os.path.exists(berkas_path):
        os.makedirs(berkas_path)

    # Inisialisasi session_state untuk menyimpan path saat ini
    if 'current_path' not in st.session_state:
        st.session_state['current_path'] = berkas_path

    # Fungsi untuk memperbarui path ke folder yang diklik
    def update_path(new_path):
        st.session_state['current_path'] = new_path

    col1, col2 = st.columns(2)
    with col1:
      # Menampilkan path saat ini
      col1 = st.write(f"📂 {st.session_state['current_path']}")
    with col2:
      # Tombol untuk kembali ke parent directory
      if st.button("Go to Parent Directory"):
        parent_path = os.path.dirname(st.session_state['current_path'])
        if os.path.commonpath([parent_path, berkas_path]) == berkas_path:  # Cegah keluar dari folder "berkas"
            st.session_state['current_path'] = parent_path

    # Mendapatkan folder dan file dari path saat ini
    folders, files = list_directory(st.session_state['current_path'])

    # Menampilkan folder dengan expander
    if folders:
        with st.expander("📁 Folders", expanded=True):
            for folder in folders:
                folder_path = os.path.join(st.session_state['current_path'], folder)
                # Menggunakan selectbox untuk update path saat folder dipilih
                if st.button(f"📁 {folder}", key=folder_path):
                    update_path(folder_path)

    # Menampilkan file dalam folder
    if files:
        with st.expander("📄 Files", expanded=True):
            for file in files:
                file_path = os.path.join(st.session_state['current_path'], file)
                with open(file_path, "rb") as f:
                    st.download_button(
                        label=f"📄 {file}",  # File dapat diklik untuk diunduh
                        data=f,
                        file_name=file
                    )

 
# Memanggil fungsi explor_arsip untuk menjalankan file explorer
#explor_arsip()
if __name__ == "__main__":
    explor_arsip()