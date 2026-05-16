from abc import ABC, abstractmethod


class ITeknologiRepository(ABC):

    @abstractmethod
    def tambah_teknologi(self, data):
        pass

    @abstractmethod
    def update_teknologi(self, data):
        pass

    @abstractmethod
    def hapus_teknologi(self, id_teknologi):
        pass

    @abstractmethod
    def get_teknologi_by_id(self, id_teknologi):
        pass

    @abstractmethod
    def get_all_teknologi(self):
        pass

    @abstractmethod
    def get_compatibility(self, nama_teknologi):
        pass