from abc import ABC, abstractmethod

class IStorageRepository(ABC):

    @abstractmethod
    def tambah_storage(self, data):
        pass

    @abstractmethod
    def ambil_storage(self, id_alternatif):
        pass

    @abstractmethod
    def update_storage(self, data):
        pass

    @abstractmethod
    def hapus_storage(self, id_alternatif):
        pass