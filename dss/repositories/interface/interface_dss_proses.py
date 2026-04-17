from abc import ABC, abstractmethod

class IDssProssesRepository(ABC):
    
    @abstractmethod
    def tambah_dss_proses(self,data):
        pass
    
    @abstractmethod
    def ambil_semua_dss_proses(self):
        pass
    