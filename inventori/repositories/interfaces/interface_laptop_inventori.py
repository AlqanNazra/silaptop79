from abc import ABC, abstractmethod

class ILaptopInventoriRepository(ABC):
    
    @abstractmethod
    def tambah_laptop_inventori(self, data):
        pass
    
    @abstractmethod
    def ambil_spek_laptop(self, id_laptop_inventori):
        pass
    
    @abstractmethod
    def ambil_laptop_inventori(self):
        pass
    
    @abstractmethod
    def ambil_hasil_saw_inventori(self, id_hasil):
        pass
    
    @abstractmethod
    def update_kondisi_inventori(self, id_laptop_inventori, kondisi):
        pass
    
    @abstractmethod
    def hapus_laptop_inventori(self, id_laptop_inventori):
        pass
    
    @abstractmethod
    def update_spek_inventori(self,id_laptop_inventori,id_processor,id_ram,id_storage):
        pass
    
    @abstractmethod
    def filter_pengadaan(self, data) -> list:
        pass