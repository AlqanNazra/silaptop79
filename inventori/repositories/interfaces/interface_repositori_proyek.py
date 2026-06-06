from abc import ABC, abstractmethod
from typing import Dict, List


class IProyekRepository(ABC):

    @abstractmethod
    def tambah(self, data):
        pass

    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def hapus(self, id_proyek):
        pass

    @abstractmethod
    def get_bobot(self, id_proyek):
        pass

    @abstractmethod
    def validate(self, id_proyek):
        pass

    @abstractmethod
    def get_roles(self, id_proyek):
        pass

    @abstractmethod
    def get_teknologi(self, id_proyek):
        pass

    @abstractmethod
    def get_summary(self, id_proyek):
        pass