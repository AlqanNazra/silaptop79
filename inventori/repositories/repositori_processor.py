import psycopg2
from psycopg2.extras import RealDictCursor
from dto.dto_processor import ProcessorDTO
from interfaces.interface_processor import IProcessorRepository


class ProcessorRepository(IProcessorRepository):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def tambah_processor(self, data: ProcessorDTO):
        query = """
        SELECT tambah_processor(%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.nama_processor,
                data.manufactur,
                data.model,
                data.cores,
                data.threads,
                data.base_clock,
                data.max_clock,
                data.arsitektur,
                data.keterangan
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # READ ALL
    # =========================
    def ambil_processor(self):
        query = "SELECT * FROM ambil_processor();"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [self._map_to_dto(row) for row in rows]

    # =========================
    # READ BY ID
    # =========================
    def ambil_precessor_by_id(self, id_processor):
        query = "SELECT * FROM ambil_processor_by_id(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_processor,))
            row = cur.fetchone()

            return self._map_to_dto(row) if row else None

    # =========================
    # UPDATE
    # =========================
    def update_processor(self, data: ProcessorDTO):
        query = """
        SELECT update_processor(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_processor if hasattr(data, "id_processor") else None,
                data.nama_processor,
                data.manufactur,
                data.model,
                data.cores,
                data.threads,
                data.base_clock,
                data.max_clock,
                data.arsitektur,
                data.keterangan
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # DELETE
    # =========================
    def hapus_processor(self, id_processor):
        query = "SELECT hapus_processor(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_processor,))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # MAPPING
    # =========================
    def _map_to_dto(self, row):
        if not row:
            return None

        dto = ProcessorDTO(
            nama_processor=row.get("nama_processor"),
            manufactur=row.get("manufacturer"),
            model=row.get("model"),
            cores=row.get("cores"),
            threads=row.get("threads"),
            base_clock=row.get("base_clock"),
            max_clock=row.get("max_clock"),
            arsitektur=row.get("arsitektur"),
            keterangan=row.get("keterangan")
        )

        # Tambahkan id kalau mau dipakai update/delete
        dto.id_processor = row.get("id_processor")

        return dto