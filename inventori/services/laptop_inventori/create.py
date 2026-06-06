from db import get_connection
from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository

class CreateLaptopInventoriService:
    def execute(self, dto):
        conn = get_connection()
        try:
            repo = LaptopInventoriRepository(conn)
            res = repo.tambah_laptop(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
