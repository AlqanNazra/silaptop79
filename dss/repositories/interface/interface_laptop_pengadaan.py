from abc import ABC, abstractmethod

class ILaptopPengadaanRepository(ABC):

    @abstractmethod
    def tambah_laptop_pengadaan(self, data):
        pass

    @abstractmethod
    def ambil_laptop_pengadaan(self):
        pass
    
    @abstractmethod
    def update_laptop_pengadaan(self, data):
        pass
    
    @abstractmethod
    def update_spek_pengadaan(self, data):
        pass

    @abstractmethod
    def hapus_laptop_pengadaan(self, id_laptop_pengadaan):
        pass

    @abstractmethod
    def ambil_hasil_saw_pengadaan(self, id_hasil):
        pass
    
    @abstractmethod
    def filter_pengadaan(self, data) -> list:
        pass
    
class ILaptopPengadaanRepositoryImpl(ILaptopPengadaanRepository):
    def __init__(self, conn):
        self.conn = conn

    def tambah_laptop_pengadaan(self, data):
        pass

    def ambil_laptop_pengadaan(self):
        pass
    
    def update_laptop_pengadaan(self, data):
        pass
    
    def update_spek_pengadaan(self, data):
        pass

    def hapus_laptop_pengadaan(self, id_laptop_pengadaan):
        pass

    def ambil_hasil_saw_pengadaan(self, id_hasil):
        pass
    
    def filter_pengadaan(self, data) -> list:
        pass