from db import get_connection
from inventori.repositories.repositori_storage import StorageRepository
from inventori.repositories.dto.dto_storage import StorageDTO

class StorageService:
    def service_tambah_storage(self, data: StorageDTO):
        conn = get_connection()
        try:
            repo = StorageRepository(conn)
            res = repo.tambah_storage(data)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def service_ambil_storage(self):
        conn = get_connection()
        try:
            repo = StorageRepository(conn)
            res = repo.ambil_storage() 
            return res
        finally:
            conn.close()
    
    def service_update_storage(self, data:StorageDTO):
        conn = get_connection()
        try:
            repo = StorageRepository(conn)
            res = repo.update_storage(data)
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def service_delete_storage(self, id_storage):
        conn = get_connection()
        try:
            repo = StorageRepository(conn)
            res = repo.hapus_storage(id_storage)
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
        
