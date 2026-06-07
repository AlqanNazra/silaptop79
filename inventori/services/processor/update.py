from core.db import get_connection
from inventori.repositories.repositori_processor import ProcessorRepository

class UpdateProcessorService:
    def execute(self, dto):
        conn = get_connection()
        try:
            repo = ProcessorRepository(conn)
            res = repo.update_processor(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
