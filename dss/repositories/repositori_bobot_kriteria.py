import psycopg2
from psycopg2.extras import RealDictCursor
from dto.dto_bobot_kriteria import BobotKriteriaDTO
from interface.interface_bobot_kriteria import IBobotkriteriaRepository

class BobotKriteriaRepository(IBobotkriteriaRepository):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def tambah_bobot_kriteria(self, data: BobotKriteriaDTO):
        query = """
        SELECT tambah_bobot_kriteria(%s, %s, %s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_kriteria,
                data.role,
                data.nilai_bobot
            ))
            self.conn.commit()

            return "Berhasil tambah bobot kriteria"

    # =========================
    # READ BY ID
    # =========================
    def cari_bobot_kriteria(self, id_bobot):
        query = "SELECT * FROM cari_bobot_kriteria(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_bobot,))
            row = cur.fetchone()

            return row

    # =========================
    # READ ALL
    # =========================
    def ambil_semua_data_detail_bobot(self):
        query = "SELECT * FROM ambil_semua_data_detail_bobot();"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return rows

    # =========================
    # UPDATE
    # =========================
    def update_bobot_kriteria(self, data: BobotKriteriaDTO):
        query = """
        SELECT update_bobot_kriteria(%s, %s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_bobot,
                data.nilai_bobot
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # DELETE
    # =========================
    def hapus_bobot_kriteria(self, id_bobot):
        query = "SELECT hapus_bobot_kriteria(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_bobot,))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None