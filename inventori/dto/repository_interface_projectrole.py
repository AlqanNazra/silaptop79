from abc import ABC, abstractmethod
from typing import List, Dict


class IProjectRoleRepository(ABC):

    @abstractmethod
    def tambah(self, data):
        pass

    @abstractmethod
    def hapus(self, id_projectrole):
        pass

    @abstractmethod
    def get_by_project(self, id_proyek):
        pass

    @abstractmethod
    def get_by_role(self, id_role):
        pass

    @abstractmethod
    def validate_relation(
        self,
        id_proyek,
        id_role
    ):
        pass