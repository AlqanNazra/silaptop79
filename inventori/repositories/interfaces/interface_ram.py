from abc import ABC, abstractmethod

class IRamRepository(ABC):

    @abstractmethod
    def tambah_ram(self, data):
        pass

    @abstractmethod
    def ambil_ram(self):
        pass

    @abstractmethod
    def update_ram(self, data):
        pass

    @abstractmethod
    def hapus_ram(self,id_ram):
        pass