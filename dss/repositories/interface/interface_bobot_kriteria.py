from abc import ABC, abstractmethod

class IBobotkriteriaRepository(ABC):

    @abstractmethod
    def tambah_bobot_kriteria(self, data):
        pass
    
    @abstractmethod
    def cari_bobot_kriteria(self, id_bobot):
        pass
    
    @abstractmethod
    def ambil_semua_data_detail_bobot(self):
        pass
    
    @abstractmethod
    def cari_bobot_kriteria_by_roles(self, role):
        pass 
    
    @abstractmethod
    def update_bobot_kriteria(self, data):
        pass
        
    @abstractmethod
    def  hapus_bobot_kriteria(self, data):
        pass
    
    @abstractmethod
    def update_nilai_swara(self, id_bobot):
        pass

class IBobotKriteriaRepositoryImpl(IBobotkriteriaRepository):
    
    def __init__(self, conn):
        self.conn = conn

    def tambah_bobot_kriteria(self, data):
        pass

    def cari_bobot_kriteria(self, id_bobot):
        pass

    def ambil_semua_data_detail_bobot(self):
        pass

    def cari_bobot_kriteria_by_roles(self, role):
        pass

    def update_bobot_kriteria(self, data):
        pass

    def hapus_bobot_kriteria(self, data):
        pass

    def update_nilai_swara(self, id_bobot):
        pass