from abc import ABC, abstractmethod

class IDetailHasilSaw(ABC):
    
    @abstractmethod
    def tambah_detail_hasil_saw(self,data):
        pass
    
    @abstractmethod
    def cari_data_detail_hasil_saw(self,id_detail):
        pass
    
    @abstractmethod
    def ambil_semua_data_detail_hasil_saw(self):
        pass
    
    @abstractmethod
    def hapus_detail_hasil_saw(self,id_detail):
        pass
    