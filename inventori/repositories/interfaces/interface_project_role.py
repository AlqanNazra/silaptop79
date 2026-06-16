from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class IProjectRoleRepository(ABC):

    @abstractmethod
    def tambah(self, data: Any) -> bool:
        pass

    @abstractmethod
    def hapus(self, id_projectrole: Any) -> bool:
        pass

    @abstractmethod
    def get_by_project(self, id_proyek: Any) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_by_role(self, id_role: Any) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def validate_relation(self, id_proyek: Any, id_role: Any) -> Optional[bool]:
        pass