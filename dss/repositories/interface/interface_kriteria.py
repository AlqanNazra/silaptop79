from abc import ABC, abstractmethod

class IKriteriaRepository(ABC):

    @abstractmethod
    def tambah_kriteria(self, data):
        pass

    @abstractmethod
    def ambil_kriteria(self):
        pass
    
    @abstractmethod
    def update_kriteria(self, data):
        pass
    @abstractmethod
    def ambil_semua_role(self):
        pass
    
class IKriteriaRepositoryImpl(IKriteriaRepository):
    def __init__(self, conn):
        self.conn = conn

    def tambah_kriteria(self, data):
        pass

    def ambil_kriteria(self):
        pass
    
    def update_kriteria(self, data):
        pass

    def ambil_semua_role(self):
        pass
    