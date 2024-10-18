import sqlite3

def buat_db():
    # Membuat koneksi ke database
    conn = sqlite3.connect('simarsip.db')
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    # Membuat tabel pengguna
    c.execute('''
    CREATE TABLE IF NOT EXISTS Pengguna (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        UnitKerja_id INTEGER NOT NULL,
        NamaUser TEXT NOT NULL,
        Passw TEXT NOT NULL,
        Nama TEXT NOT NULL,
        NIP TEXT NOT NULL,
        FOREIGN KEY (UnitKerja_id) REFERENCES UnitKerja(id) ON DELETE CASCADE
    )
    ''')

    # Membuat tabel unit kerja
    c.execute('''
    CREATE TABLE IF NOT EXISTS UnitKerja (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        IdUnit TEXT NOT NULL,
        NamaUnit TEXT NOT NULL,
        Inisial TEXT NOT NULL,
        NamaJabatan TEXT NOT NULL,
        NamaPejabat TEXT NOT NULL,
        NIPPejabat TEXT NOT NULL
    )
    ''')

    # Membuat tabel Nomor Surat
    c.execute('''
    CREATE TABLE IF NOT EXISTS NoSurat (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        UnitKerja_id INTEGER NOT NULL,
        Pengguna_id INTEGER NOT NULL,
        Nama_Pengguna TEXT NOT NULL,
        TglSurat TEXT NOT NULL,
        Tahun TEXT NOT NULL,
        No INTEGER NOT NULL,
        Hal TEXT NOT NULL,
        KA TEXT NOT NULL,
        No_Surat TEXT NOT NULL,
        Status INTEGER NOT NULL DEFAULT 0,
        Lokasi TEXT,
        FOREIGN KEY (UnitKerja_id) REFERENCES UnitKerja(id) ON DELETE CASCADE,
        FOREIGN KEY (Pengguna_id) REFERENCES Pengguna(id) ON DELETE CASCADE
    )
    ''')

    # Membuat tabel Klasifikasi Arsip
    c.execute('''
    CREATE TABLE IF NOT EXISTS KA (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ParentId INTEGER NOT NULL,
        Kd TEXT NOT NULL,
        Fungsi TEXT NOT NULL,
        Kode TEXT NOT NULL,
        Nama TEXT NOT NULL,
        Deskripsi TEXT,
        RetAktif INTEGER,
        KetRetAktif TEXT,
        RetInAktif INTEGER,
        KetRetInAktif TEXT,
        StatusRetensi TEXT,
        KetStatusRetensi TEXT,
        KetSKKA TEXT,
        SKKA TEXT,
        Pengguna TEXT
    )
    ''')

    # Membuat tabel Berkas
    c.execute('''
    CREATE TABLE IF NOT EXISTS Berkas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        KA_id INTEGER NOT NULL,
        Tahun TEXT NOT NULL,
        NoBerkas TEXT NOT NULL,
        KodeKA TEXT NOT NULL,
        UraianInformasiBerkas TEXT NOT NULL,
        Waktu1 TEXT NOT NULL,
        Waktu2 TEXT NOT NULL,
        Jumlah TEXT NOT NULL,
        Ket TEXT NOT NULL,
        Lokasi TEXT NOT NULL,
        RetAktif INTEGER NOT NULL,
        KetRetAktif TEXT NOT NULL,
        RetInAktif INTEGER NOT NULL,
        KetRetInAktif TEXT NOT NULL,
        StatusRetensi TEXT NOT NULL,
        TglClose DATE,
        TglMulaiAktif DATE,
        TglMulaiPindah DATE,
        Status TEXT,
        TglBAPInAktif DATE,
        NoBAPInaktif TEXT,    
        TglMusnah_Serah DATE,
        NoBAPMusnah_Serah DATE,
        LokasiInaktif TEXT,
        KetSKKA TEXT,
        NoBoks TEXT,
        FOREIGN KEY (KA_id) REFERENCES KA(id) ON DELETE CASCADE
    )
    ''')

    # Membuat tabel Arsip Keluar
    c.execute('''
    CREATE TABLE IF NOT EXISTS ArsipOut (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Pengguna_id INTEGER NOT NULL,
        UnitKerja_id INTEGER NOT NULL,
        KA_id INTEGER NOT NULL,
        Berkas_id INTEGER NOT NULL,
        NomorSurat INTEGER NOT NULL,
        TglSurat DATE NOT NULL,    
        Kode TEXT NOT NULL,
        Jenis TEXT NOT NULL,
        Hal TEXT NOT NULL,
        IsiSurat TEXT,
        Lampiran INTEGER,
        Ttd TEXT NULL,
        Direktori TEXT NULL,
        NamaFile TEXT NULL,
        Status TEXT NULL,
        TMTAktif DATE,
        TMTInAktif DATE,
        TMTStatis DATE,
        TMTMusnah DATE,
        TMTPindah DATE,
        TMTSerah DATE,
        NoItem INTEGER,
        KetSKKA TEXT,
        Retensi TEXT,
        RetAktif INTEGER,
        RetInaktif INTEGER,
        Lokasi TEXT,
        TglEntri DATE NOT NULL,
        Pengguna TEXT,
        TAHUN TEXT,
        FOREIGN KEY (Pengguna_id) REFERENCES Pengguna(id) ON DELETE CASCADE,
        FOREIGN KEY (UnitKerja_id) REFERENCES UnitKerja(id) ON DELETE CASCADE
        FOREIGN KEY (KA_id) REFERENCES KA(id) ON DELETE CASCADE
        FOREIGN KEY (Berkas_id) REFERENCES Berkas(id) ON DELETE CASCADE
    )
    ''')

    # Membuat tabel Arsip Keluar
    c.execute('''
    CREATE TABLE IF NOT EXISTS ArsipIn (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Pengguna_id INTEGER NOT NULL,
        UnitKerja_id INTEGER NOT NULL,
        KA_id INTEGER NOT NULL,
        Berkas_id INTEGER NOT NULL,
        NomorSurat INTEGER NOT NULL,
        TglSurat DATE NOT NULL,    
        Kode TEXT NOT NULL,
        Jenis TEXT NOT NULL,
        Hal TEXT NOT NULL,
        IsiSurat TEXT,
        Lampiran INTEGER,
        Ttd TEXT NULL,
        Direktori TEXT NULL,
        NamaFile TEXT NULL,
        Status TEXT NULL,
        TMTAktif DATE,
        TMTInAktif DATE,
        TMTStatis DATE,
        TMTMusnah DATE,
        TMTPindah DATE,
        TMTSerah DATE,
        NoItem INTEGER,
        KetSKKA TEXT,
        Retensi TEXT,
        RetAktif INTEGER,
        RetInaktif INTEGER,
        Lokasi TEXT ,
        TglEntri DATE NOT NULL,
        Pengirim TEXT,
        Pengguna TEXT,
        TAHUN TEXT,
        FOREIGN KEY (Pengguna_id) REFERENCES Pengguna(id) ON DELETE CASCADE,
        FOREIGN KEY (UnitKerja_id) REFERENCES UnitKerja(id) ON DELETE CASCADE
        FOREIGN KEY (KA_id) REFERENCES KA(id) ON DELETE CASCADE
        FOREIGN KEY (Berkas_id) REFERENCES Berkas(id) ON DELETE CASCADE
    )
    ''')

    # Membuat tabel cuti
    c.execute('''
    CREATE TABLE IF NOT EXISTS cuti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mhs_id INTEGER NOT NULL,
        semester TEXT NOT NULL,
        ThnAkademik TEXT NOT NULL,
        Prodi TEXT NOT NULL,
        Keperluan TEXT NOT NULL,
        FOREIGN KEY (mhs_id) REFERENCES mhs(id) ON DELETE CASCADE
    )
    ''')
    return
buat_db()