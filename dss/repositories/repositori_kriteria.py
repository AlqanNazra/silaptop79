import psycopg2
from psycopg2.extras import RealDictCursor
from .dto.dto_kriteria import KriteriaDTO
from .interface.interface_kriteria import IKriteriaRepositoryImpl


class KriteriaRepository(IKriteriaRepositoryImpl):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def tambah_kriteria(self, data: KriteriaDTO):
        query = """
        SELECT tambah_kriteria(%s, %s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.nama_kriteria,
                data.tipe_kriteria,
            ))

            id_kriteria = cur.fetchone()[0]

            self.conn.commit()

            return id_kriteria

    # =========================
    # READ
    # =========================
    def ambil_kriteria(self):
        query = "SELECT * FROM ambil_kriteria();"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return rows  # langsung dict (lebih fleksibel untuk frontend)

    # =========================
    # UPDATE
    # =========================
    def update_kriteria(self, data: KriteriaDTO):
        query = """
        SELECT update_kriteria(%s, %s, %s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_kriteria,
                data.nama_kriteria,
                data.tipe_kriteria
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None