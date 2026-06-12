from abc import ABC, abstractmethod


class IProyekService(ABC):

    @abstractmethod
    def tambah_proyek(self, data):
        pass

    @abstractmethod
    def update_proyek(self, data):
        pass

    @abstractmethod
    def hapus_proyek(self, id_proyek):
        pass

    @abstractmethod
    def calculate_project_requirement(self, id_proyek):
        pass