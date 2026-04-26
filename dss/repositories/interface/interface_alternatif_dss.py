from abc import ABC, abstractmethod

class IAlternatifDss(ABC):
    
    @abstractmethod
    def tambah_alternatif_dss(self,data):
        pass
    
    @abstractmethod
    def cari_alternatif_dss(self,id_alternatif):
        pass
    
    @abstractmethod
    def hapus_alternatif_dss(self, id_alternatif):
        pass
    
class IAlternatifDssImpl(IAlternatifDss):
    def __init__(self, conn):
        self.conn = conn

    def tambah_alternatif_dss(self,data):
        pass

    def cari_alternatif_dss(self,id_alternatif):
        pass

    def hapus_alternatif_dss(self, id_alternatif):
        pass