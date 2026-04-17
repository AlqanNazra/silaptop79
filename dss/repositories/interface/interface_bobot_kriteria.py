from abc import ABC, abstractmethod

class IBobotkriteriaRepository(ABC):

    @abstractmethod
    def tambah_bobot_kriteria(delf, data):
        pass
    
    @abstractmethod
    def cari_bobot_kriteria(self, id_bobot):
        pass
    
    @abstractmethod
    def ambil_semua_data_detail_bobot(self):
        pass
    
    @abstractmethod
    def update_bobot_kriteria(self, data):
        pass
        
    @abstractmethod
    def  hapus_bobot_kriteria(self, f_id_bobot):
        pass