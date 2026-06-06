from db import get_connection
from inventori.repositories.repositori_laptop_inventori import LaptopInventoriRepository

class UpdateLaptopInventoriService:
    def update_kondisi(self, id_laptop, kondisi):
        conn = get_connection()
        try:
            repo = LaptopInventoriRepository(conn)
            res = repo.update_kondisi(id_laptop, kondisi)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def update_status(self, id_laptop, status, lokasi=None):
        conn = get_connection()
        try:
            repo = LaptopInventoriRepository(conn)
            res = repo.update_status(id_laptop, status, lokasi)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def update_spek(self, dto):
        conn = get_connection()
        try:
            repo = LaptopInventoriRepository(conn)
            res = repo.update_spek(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
