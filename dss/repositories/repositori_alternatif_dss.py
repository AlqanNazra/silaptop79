import psycopg2
from psycopg2.extras import RealDictCursor
from dss.dto.dto_alternatif_dss import AlternatifDssDTO
from interface.interface_alternatif_dss import IAlternatifDss


class AlternatifDssRepository(IAlternatifDss):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def tambah_alternatif_dss(self, data: AlternatifDssDTO):
        query = """
        SELECT tambah_alternatif_dss(%s, %s, %s, %s, %s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_alternatif,
                data.id_dss,
                data.id_laptop_pengadaan,
                data.id_laptop_inventori,
                data.sumber_data
            ))
            self.conn.commit()

            return "Berhasil tambah alternatif DSS"

    # =========================
    # READ BY ID
    # =========================
    def cari_alternatif_dss(self, id_alternatif):
        query = "SELECT * FROM cari_alternatif_dss(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_alternatif,))
            row = cur.fetchone()

            return row

    # =========================
    # DELETE
    # =========================
    def hapus_alternatif_dss(self, id_alternatif):
        query = "SELECT hapus_alternatif_dss(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_alternatif,))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None