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
    