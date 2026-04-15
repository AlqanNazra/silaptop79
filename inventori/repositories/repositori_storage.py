from .base_repository import BaseRepository
from .interfaces.interface_storage import IStorageRepository
from .dto.dto_storage import StorageDTO


class AlternatifDSSRepository(BaseRepository, IStorageRepository):

    def tambah_storage(self, data: StorageDTO) -> str:
        query = "SELECT tambah_storage(%s, %s)"

        result = self.execute(
            query,
            [
                data.kapasitas_gb,
                data.tipe,
            ],
            fetch_one=True
        )

        return result[0] if result else None


    def get_by_id(self):
        query = "SELECT * FROM ambil_storage()"

        result = self.execute(
            query,
            fetch_all=True
        )

        return result


    def update(self, data: StorageDTO) -> str:
        query = "SELECT update_storage(%s, %s)"

        result = self.execute(
            query,
            [
                data.kapasitas_gb,
                data.tipe,
            ],
            fetch_one=True
        )

        return result[0] if result else None


    def delete(self, id_storage: str) -> str:
        query = "SELECT hapus_storage(%s)"

        result = self.execute(
            query,
            [id_storage],
            fetch_one=True
        )

        return result[0] if result else None