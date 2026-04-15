from abc import ABC, abstractmethod

class IPeminjamanRepository(ABC):
    
    @abstractmethod
    def tambah_peminjaman(self, data):
        pass
    
    @abstractmethod
    def ambil_semua_peminjaman(self):
        pass
    
    @abstractmethod
    def cari_peminjaman(self,id_peminjaman):
        pass
    
    @abstractmethod
    def update_peminjaman(self, data):
        pass
    
    @abstractmethod
    def hapus_peminjaman(self, id_peminjaman):
        pass
    
    @abstractmethod
    def pinjam_laptop(self,data):
        pass
    
    @abstractmethod
    def pengembalian_laptop(self,data):
        pass
    
    @abstractmethod
    def sync_status_laptop(self):
        pass
    
    @abstractmethod
    def ambil_laptop_by_lokasi(self,data):
        pass