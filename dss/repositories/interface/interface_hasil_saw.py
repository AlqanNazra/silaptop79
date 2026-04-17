from abc import ABC, abstractmethod

class IHasilSawRepository(ABC):
    @abstractmethod
    def buat_hasil_saw (self,id_dss):
        pass