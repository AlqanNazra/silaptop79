from abc import ABC, abstractmethod

class ILaptopInventoriRepository(ABC):
    @abstractmethod
    def tambah_laptop(self, dto):
        pass

    @abstractmethod
    def ambil_laptop(self):
        pass

    @abstractmethod
    def ambil_spek_laptop(self, id_laptop):
        pass

    @abstractmethod
    def update_kondisi(self, id_laptop, kondisi):
        pass

    @abstractmethod
    def update_status(self, id_laptop, status, lokasi):
        pass

    @abstractmethod
    def update_spek(self, dto):
        pass

    @abstractmethod
    def hapus_laptop(self, id_laptop):
        pass
