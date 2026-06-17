from ..repositories.interface.interface_laptop_pengadaan import ILaptopPengadaanRepositoryImpl
from ..repositories.dto.dto_laptop_pengadaan import LaptopPengadaanDTO


class LaptopPengadaanService:

    def __init__(self, repo: ILaptopPengadaanRepositoryImpl):
        self.repo = repo

    def tambah_laptop(self, data: LaptopPengadaanDTO):
        # validasi sederhana
        if not data.nama_laptop:
            raise ValueError("Nama laptop tidak boleh kosong")

        return self.repo.tambah_laptop_pengadaan(data)

    def get_all_laptop(self):
        return self.repo.ambil_laptop_pengadaan()

    def update_laptop(self, data: LaptopPengadaanDTO):
        if not data.id_laptop_pengadaan:
            raise ValueError("ID wajib diisi")

        return self.repo.update_laptop_pengadaan(data)

    def update_spek(self, data: LaptopPengadaanDTO):
        return self.repo.update_spek_pengadaan(data)

    def hapus_laptop(self, id_laptop_pengadaan: str):
        return self.repo.hapus_laptop_pengadaan(id_laptop_pengadaan)

    def get_hasil_saw(self, id_hasil):
        return self.repo.ambil_hasil_saw_pengadaan(id_hasil)