import psycopg2
from psycopg2.extras import RealDictCursor
from dss.dto.dto_detail_hasil_saw import DetailHasilSawDTO
from interface.interface_detail_hasil_saw import IDetailHasilSawImpl


class DetailHasilSawRepository(IDetailHasilSawImpl):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def tambah_detail_hasil_saw(self, data: DetailHasilSawDTO):
        query = """
        SELECT tambah_detail_hasil_saw(%s, %s, %s, %s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_hasil,
                data.nilai_normalisasi,
                data.nilai_rangking,
                data.rangking
            ))
            self.conn.commit()

            return "Berhasil tambah detail hasil SAW"

    # =========================
    # READ BY ID
    # =========================
    def cari_data_detail_hasil_saw(self, id_detail):
        query = "SELECT * FROM cari_data_detail_hasil_saw(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_detail,))
            row = cur.fetchone()

            return row

    # =========================
    # READ ALL
    # =========================
    def ambil_semua_data_detail_hasil_saw(self):
        query = "SELECT * FROM ambil_semua_data_detail_hasil_saw();"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return rows

    # =========================
    # DELETE
    # =========================
    def hapus_detail_hasil_saw(self, id_detail):
        query = "SELECT hapus_detail_hasil_saw(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_detail,))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None