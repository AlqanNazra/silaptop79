from abc import ABC, abstractmethod

class IDssProssesRepository(ABC):
    
    @abstractmethod
    def tambah_dss_proses(self,data):
        pass
    
    @abstractmethod
    def ambil_semua_dss_proses(self):
        pass

class IDssProssesRepositoryImpl(IDssProssesRepository):
    def __init__(self, conn):
        self.conn = conn

    def tambah_dss_proses(self,data):
        pass

    def ambil_semua_dss_proses(self):
        pass
    