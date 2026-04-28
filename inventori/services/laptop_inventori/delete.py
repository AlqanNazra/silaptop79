from core.db import get_connection
from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository

class DeleteLaptopInventoriService:
    def execute(self, id_laptop):
        conn = get_connection()
        try:
            repo = LaptopInventoriRepository(conn)
            res = repo.hapus_laptop(id_laptop)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
