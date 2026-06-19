import psycopg2
from psycopg2.extras import RealDictCursor
from .dto.dto_dss_proses import DssProsesDTO
from .interface.interface_dss_proses import IDssProssesRepositoryImpl 


class DssprossesRepository(IDssProssesRepositoryImpl):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def tambah_dss_proses(self, data: DssProsesDTO):

        query = """
        SELECT tambah_dss_proses(%s, %s, %s, %s);
        """

        with self.conn.cursor() as cur:

            cur.execute(
                query,
                (
                    data.id_user,
                    data.id_bobot,
                    data.role_dss,
                    data.jenis_dss
                )
            )

            hasil = cur.fetchone()

            # print("\n=== DEBUG HASIL DSS ===")
            # print(hasil)
            # print(type(hasil))

            self.conn.commit()

            # Cursor biasa
            if isinstance(hasil, tuple):
                return hasil[0]

            # RealDictCursor
            if isinstance(hasil, dict):
                return next(iter(hasil.values()))

            return hasil   
    # =========================
    # Ambil Semua
    # =========================
    def ambil_semua_dss_proses(self):
        query = "SELECT * FROM ambil_semua_dss_proses()"
        
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
        
        return rows