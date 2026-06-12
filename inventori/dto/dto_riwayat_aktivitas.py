class RiwayatAktivitasDTO:
    def __init__(self, id_aktivitas = None, id_user = None, id_laptop = None, jenis_aktivitas = None
                 ,keterangan = None, nama_aset = None, role_pengguna = None):
        self.id_aktivitas = id_aktivitas
        self.id_user = id_user
        self.id_laptop = id_laptop
        self.jenis_aktivitas = jenis_aktivitas
        self.keterangan = keterangan
        self.nama_aset = nama_aset
        self.role_pengguna = role_pengguna