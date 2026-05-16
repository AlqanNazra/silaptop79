from db import get_connection
from inventori.repositories.repositori_ram import RamRepository
from inventori.repositories.dto.dto_ram import RamDTO

class RamService:
    def service_tambah_ram(self,dto: RamDTO):
        conn = get_connection()
        try:
            repo = RamRepository(conn)
            res = repo.tambah_ram(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def service_ambil_ram(self):
        conn = get_connection()
        try:
            repo = RamRepository(conn)
            res = repo.ambil_ram()
            return res
        finally:
            conn.close()
    
    def service_update_ram(self, data: RamDTO):
        conn = get_connection()
        try:
            repo = RamRepository(conn)
            res = repo.update_ram(data)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
            
    def service_hapus_ram(self,id_ram):
        conn = get_connection()
        try:
            repo = RamRepository(conn)
            res = repo.hapus_ram(id_ram)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        