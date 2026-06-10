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
        print("➡️ QUERY TAMBAH KRITERIA DTO")

        query = "SELECT tambah_kriteria(%s, %s, %s,%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.nama_kriteria,
                data.tipe_kriteria,
                data.golongan_kriteria
            ))

            result = cur.fetchone()
            print("RESULT KRITERIA:", result)

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None

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

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None
        
    def ambil_semua_role(self):
        query = "SELECT role FROM dss_bobotkriteria;"

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [row[0] for row in rows]