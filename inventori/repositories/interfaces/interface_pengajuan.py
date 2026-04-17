from abc import ABC, abstractmethod

class IPengajuanRepository(ABC):

    @abstractmethod
    def tambah_pengajuan(self, data):
        pass

    @abstractmethod
    def ambil_semua_pengajuan(self):
        pass

    @abstractmethod
    def cari_pengajuan(self, id_pengajuan):
        pass

    @abstractmethod
    def hapus_pengajuan(self, id_pengajuan):
        pass

    @abstractmethod
    def approve_pengajuan(self, data):
        pass