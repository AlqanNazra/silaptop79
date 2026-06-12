class PeminjamanDTO:
    def __init__(self,
                 id_peminjaman=None,id_pengajuan=None,id_user=None,id_laptop_inventori=None,tanggal_pinjam=None,
                 tanggal_kembali=None,status=None,keterangan=None):
        self.id_peminjaman = id_peminjaman
        self.id_pengajuan = id_pengajuan
        self.id_user = id_user
        self.id_laptop_inventori = id_laptop_inventori
        self.tanggal_pinjam = tanggal_pinjam
        self.tanggal_kembali = tanggal_kembali
        self.status = status
        self.keterangan = keterangan