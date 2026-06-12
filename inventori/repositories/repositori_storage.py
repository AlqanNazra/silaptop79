from .base_repository import BaseRepository
from .interfaces.interface_storage import IStorageRepository
from .dto.dto_storage import StorageDTO
from psycopg2.extras import RealDictCursor

class StorageRepository(BaseRepository, IStorageRepository):
    
    def __init__(self, conn):
        self.conn = conn

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


    def ambil_storage(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM ambil_storage()")
            return cur.fetchall()


    def update_storage(self, data: StorageDTO) -> str:
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


    def delete_storage(self, id_storage: str) -> str:
        query = "SELECT hapus_storage(%s)"

        result = self.execute(
            query,
            [id_storage],
            fetch_one=True
        )

        return result[0] if result else None