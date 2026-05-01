import psycopg2
from psycopg2.extras import RealDictCursor
from .dto.dto_bobot_kriteria import BobotKriteriaDTO
from .interface.interface_bobot_kriteria import IBobotKriteriaRepositoryImpl

class BobotKriteriaRepository(IBobotKriteriaRepositoryImpl):

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
                str(data.id_kriteria),
                data.role,
                data.nilai_bobot
            ))

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
        
    def ambil_bobot_by_kriteria(self, id_bobot, id_kriteria):
        query = "SELECT * FROM ambil_bobot_by_kriteria(%s, %s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_bobot, id_kriteria))
            rows = cur.fetchall()

            return rows
        
    def cari_bobot_kriteria_by_roles(self, roles: list):
        print("FUNCTION REPO KE PANGGIL")  # 🔥 WAJIB MUNCUL
        query = "SELECT * FROM cari_bobot_kriteria_by_roles(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (roles,))  # psycopg2 otomatis handle array
            rows = cur.fetchall()

            return rows

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

            return result[0] if result else None
        
    def update_nilai_swara(self, data: BobotKriteriaDTO):
        query = "SELECT update_nilai_swara(%s, %s)"
        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_bobot,
                data.nilai_swara
            ))
            result = cur.fetchone()

            return result[0] if result else None

    # =========================
    # DELETE
    # =========================
    def hapus_bobot_kriteria(self, id_bobot):
        query = "SELECT hapus_bobot_kriteria(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_bobot,))
            result = cur.fetchone()

            return result[0] if result else None