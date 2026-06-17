# interfaces/role_interface.py
from abc import ABC, abstractmethod
from typing import List, Dict

class IRoleRepository(ABC):
    @abstractmethod
    def tambah(self, data) -> str: pass

    @abstractmethod
    def update(self, data) -> bool: pass

    @abstractmethod
    def hapus(self, id_role: str) -> bool: pass

    @abstractmethod
    def get_kriteria(self, id_role: str) -> List[Dict]: pass

    @abstractmethod
    def get_teknologi(self, id_role: str) -> List[Dict]: pass


class IRoleService(ABC):
    @abstractmethod
    def tambah_role(self, data) -> str: pass

    @abstractmethod
    def update_role(self, data) -> bool: pass

    @abstractmethod
    def hapus_role(self, id_role: str) -> bool: pass

    # @abstractmethod
    # def calculate_need_score(self, id_role: str) -> Dict: pass