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