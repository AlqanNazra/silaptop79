from abc import ABC, abstractmethod


class IRoleTeknologiRepository(ABC):

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(
        self,
        id_role_teknologi
    ):
        pass

    @abstractmethod
    def tambah(self, data):
        pass

    @abstractmethod
    def hapus(
        self,
        id_role_teknologi
    ):
        pass