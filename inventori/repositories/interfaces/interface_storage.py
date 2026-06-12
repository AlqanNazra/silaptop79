from abc import ABC, abstractmethod

class IStorageRepository(ABC):

    @abstractmethod
    def tambah_storage(self, data):
        pass

    @abstractmethod
    def ambil_storage(self):
        pass

    @abstractmethod
    def update_storage(self, data):
        pass

    @abstractmethod
    def delete_storage(self, id_alternatif):
        pass