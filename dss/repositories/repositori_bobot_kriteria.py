from django.db import connection
import psycopg2
from psycopg2.extras import RealDictCursor
from .dto.dto_bobot_kriteria import BobotKriteriaDTO
from .interface.interface_bobot_kriteria import IBobotKriteriaRepositoryImpl

class BobotKriteriaRepository(IBobotKriteriaRepositoryImpl):

    def __init__(self, conn):
        self.conn = conn

    def _get_dict_cursor(self):
        try:
            return self.conn.cursor(cursor_factory=RealDictCursor)
        except TypeError:
            return self.conn.cursor()

    def _format_result(self, cur, rows_or_row, fetch_all=True):
        if hasattr(cur, 'description') and cur.description and not type(cur).__name__ == 'RealDictCursor':
            columns = [col[0] for col in cur.description]
            if fetch_all:
                return [dict(zip(columns, row)) for row in rows_or_row]
            else:
                return dict(zip(columns, rows_or_row)) if rows_or_row else None
        return rows_or_row

    # =========================
    # CREATE
    # =========================
    def tambah_bobot_kriteria(self,data: BobotKriteriaDTO):
        query = """SELECT tambah_bobot_kriteria(%s,%s,%s);"""
        print("\nSQL INSERT BOBOT")
        print(
            data.id_role_teknologi,
            data.id_kriteria,
            data.nilai_bobot
        )
        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (
                    data.id_role_teknologi,
                    data.id_kriteria,
                    data.nilai_bobot
                )
            )
            result = cur.fetchone()
            print(
                "DB RESULT:",
                result
            )
            if result:
                if isinstance(result, dict):
                    return list(
                        result.values()
                    )[0]
                return result[0]
            return None

    # =========================
    # READ BY ID
    # =========================
    def cari_bobot_kriteria(self, id_bobot):
        query = "SELECT * FROM cari_bobot_kriteria(%s);"

        with self._get_dict_cursor() as cur: # 🔄 Menggunakan helper
            cur.execute(query, (id_bobot,))
            row = cur.fetchone()

            return self._format_result(cur, row, fetch_all=False) # 🔄 Format hasil
        
    def ambil_bobot_by_kriteria(self, id_bobot, id_kriteria):
        query = "SELECT * FROM ambil_bobot_by_kriteria(%s, %s);"

        with self._get_dict_cursor() as cur: # 🔄 Menggunakan helper
            cur.execute(query, (id_bobot, id_kriteria))
            rows = cur.fetchall()

            return self._format_result(cur, rows, fetch_all=True) # 🔄 Format hasil
        
    def cari_bobot_kriteria_by_roles(self, roles: list):
        print("FUNCTION REPO KE PANGGIL")  # 🔥 WAJIB MUNCUL
        query = "SELECT * FROM cari_bobot_kriteria_by_roles(%s);"

        with self._get_dict_cursor() as cur: # 🔄 Menggunakan helper
            cur.execute(query, (roles,))  # psycopg2 otomatis handle array
            rows = cur.fetchall()

            return self._format_result(cur, rows, fetch_all=True) # 🔄 Format hasil

    # =========================
    # READ ALL
    # =========================
    def ambil_semua_data_detail_bobot(self):
        query = "SELECT * FROM ambil_semua_data_detail_bobot();"

        with self._get_dict_cursor() as cur: # 🔄 Menggunakan helper
            cur.execute(query)
            rows = cur.fetchall()

            return self._format_result(cur, rows, fetch_all=True) # 🔄 Format hasil

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

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None
        
    def update_nilai_swara(self, data):

        query = """
        SELECT update_nilai_swara(
            %s,
            %s
        )
        """

        print(
            "UPDATE PARAM",
            data.id_bobot,
            data.nilai_swara
        )

        with self.conn.cursor() as cur:

            cur.execute(
                query,
                (
                    data.id_bobot,
                    data.nilai_swara
                )
            )

            result = cur.fetchone()

            self.conn.commit()

            print(
                "DB RESULT",
                result
            )

            return result[0]

    # =========================
    # DELETE
    # =========================
    def hapus_bobot_kriteria(self, id_bobot):
        query = "SELECT hapus_bobot_kriteria(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_bobot,))
            result = cur.fetchone()

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None
        
    def ambil_bobot_role_teknologi(
        self,
        id_role_teknologi
    ):
        query = """
            SELECT
                bk.id_bobot,
                bk.id_kriteria,
                k.nama_kriteria,
                bk.nilai_bobot,
                bk.nilai_swara
            FROM dss_bobotkriteria bk
            JOIN dss_kriteria k
                ON k.id_kriteria = bk.id_kriteria
            WHERE bk.id_role_teknologi = %s
            AND bk.is_active = TRUE
            ORDER BY bk.nilai_bobot DESC
        """

        with self._get_dict_cursor() as cur:
            cur.execute(
                query,
                (id_role_teknologi,)
            )

            return cur.fetchall()
        
    def update_bobot_role_teknologi(
        self,
        data
    ):

        query = """
        UPDATE dss_bobotkriteria
        SET

            nilai_bobot = %s

        WHERE

            id_role_teknologi = %s

            AND

            id_kriteria = %s

            AND

            is_active = TRUE
        """

        with self.conn.cursor() as cur:

            cur.execute(

                query,

                (
                    data.nilai_bobot,

                    data.id_role_teknologi,

                    data.id_kriteria
                )
            )
            print(
            data.id_role_teknologi,
            data.id_kriteria,
            data.nilai_bobot
        )
            print("ROW UPDATED:",cur.rowcount)

        return True