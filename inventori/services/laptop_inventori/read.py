from core.db import get_connection
from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository

class ReadLaptopInventoriService:
    def ambil_semua(self):
        conn = get_connection()
        try:
            repo = LaptopInventoriRepository(conn)
            return repo.ambil_laptop()
        finally:
            conn.close()

    def ambil_spek_by_id(self, id_laptop):
        conn = get_connection()
        try:
            repo = LaptopInventoriRepository(conn)
            return repo.ambil_spek_laptop(id_laptop)
        finally:
            conn.close()
