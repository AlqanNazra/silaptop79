from abc import ABC, abstractmethod

class IRiwayatAktivitasRepository(ABC):

    @abstractmethod
    def tambah_riwayat_aktivitas(self, data):
        pass
    
    @abstractmethod
    def ambil_semua_riwayat(self):
        pass
    
    @abstractmethod
    def ambil_cari_riwayat(self, id_aktvitas):
        pass

    @abstractmethod
    def ambil_cari_riwayat_laptop(self, id_laptop_inventori):
        pass
    
    @abstractmethod
    def ambil_cari_riwayat_user(self, id_user):
        pass
    @abstractmethod
    def ambil_cari_riwayat_tanggal(self, tanggal):
        pass
    @abstractmethod
    def ambil_cari_riwayat_jenis(self, jenis_aktivitas):
        pass
    @abstractmethod
    def ambil_cari_riwayat_filter_riwayat(self, id_laptop_inventori,id_user,tanggal,jenis_aktivitas):
        pass

    @abstractmethod
    def hapus_riwayat_aktivitas(self, id_aktivitas):
        pass