from db import get_connection
from inventori.repositories.repositori_processor import ProcessorRepository

class ReadProcessorService:

    def ambil_processor(self):
        conn = get_connection()
        try:
            repo = ProcessorRepository(conn)
            return repo.ambil_processor()
        finally:
            conn.close()

    def ambil_by_id(self, id_processor):
        conn = get_connection()
        try:
            repo = ProcessorRepository(conn)
            return repo.ambil_processor_by_id(id_processor)
        finally:
            conn.close()