from core.db import get_connection
from inventori.repositories.repositori_processor import ProcessorRepository

class DeleteProcessorService:
    def execute(self, id_processor):
        conn = get_connection()
        try:
            repo = ProcessorRepository(conn)
            res = repo.hapus_processor(id_processor)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
