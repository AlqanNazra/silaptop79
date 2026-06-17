from abc import ABC, abstractmethod

class IHasilSawRepository(ABC):
    @abstractmethod
    def buat_hasil_saw (self,id_dss):
        pass
    
class IHasilSawRepositoryImpl(IHasilSawRepository):
    def __init__(self, conn):
        self.conn = conn

    def buat_hasil_saw (self,id_dss):
        pass