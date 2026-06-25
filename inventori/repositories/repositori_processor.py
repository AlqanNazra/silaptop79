from inventori.repositories.interfaces.interface_processor import IProcessorRepository
from psycopg2.extras import RealDictCursor
class ProcessorRepository(IProcessorRepository):
    def __init__(self, connection):
        self.conn = connection

    def tambah_processor(self, dto):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT tambah_processor(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (dto.nama_processor, dto.manufacturer, dto.model, dto.cores, 
                  dto.threads, dto.base_clock, dto.max_clock, dto.arsitektur, dto.keterangan))
            return cur.fetchone()['tambah_processor']

    def ambil_processor(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM ambil_processor()")
            return cur.fetchall()

    def ambil_processor_by_id(self, id_processor):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM ambil_processor_by_id(%s)", (id_processor,))
            return cur.fetchone()

    def update_processor(self, dto):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT update_processor(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (dto.id_processor, dto.nama_processor, dto.manufacturer, dto.model, 
                  dto.cores, dto.threads, dto.base_clock, dto.max_clock, dto.arsitektur, dto.keterangan))
            return cur.fetchone()['update_processor']

    def hapus_processor(self, id_processor):
        with self.conn.cursor() as cur:
            cur.execute("SELECT hapus_processor(%s)", (id_processor,))
            return cur.fetchone()['hapus_processor']
    
    from psycopg2.extras import RealDictCursor


    def ambil_processor_dropdown(self):

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute("""
                SELECT
                    id_processor,
                    nama_processor,
                    processor_score
                FROM inventori_processor
                ORDER BY nama_processor
            """)

            return cur.fetchall()