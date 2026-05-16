from abc import ABC, abstractmethod


class IProjectRoleService(ABC):

    @abstractmethod
    def tambah_projectrole(self, data):
        pass

    @abstractmethod
    def hapus_projectrole(self, id_projectrole):
        pass

    @abstractmethod
    def getByProject(self, id_proyek):
        pass

    @abstractmethod
    def getByRole(self, id_role):
        pass

    @abstractmethod
    def validateRelation(
        self,
        id_proyek,
        id_role
    ):
        pass