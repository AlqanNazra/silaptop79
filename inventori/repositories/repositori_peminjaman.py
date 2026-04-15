import psycopg2
from psycopg2.extras import RealDictCursor
from dto.dto_peminjaman import PeminjamanDTO
from interfaces.interface_peminjaman import IPeminjamanRepository


class PeminjamanRepository(IPeminjamanRepository):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def tambah_peminjaman(self, data: PeminjamanDTO):
        query = """
        SELECT tambah_peminjaman(%s,%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_user,
                data.id_laptop_inventori,
                data.tanggal_pinjam,
                data.tanggal_kembali,
                data.status,
                data.keterangan
            ))
            self.conn.commit()

            return "Berhasil tambah peminjaman"

    # =========================
    # READ ALL
    # =========================
    def ambil_semua_peminjaman(self):
        query = "SELECT * FROM ambil_semua_peminjaman();"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [self._map_to_dto(row) for row in rows]

    # =========================
    # READ BY ID
    # =========================
    def cari_peminjaman(self, id_peminjaman):
        query = "SELECT * FROM cari_peminjaman(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_peminjaman,))
            row = cur.fetchone()

            return self._map_to_dto(row) if row else None

    # =========================
    # UPDATE
    # =========================
    def update_peminjaman(self, data: PeminjamanDTO):
        query = """
        SELECT update_peminjaman(%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_peminjaman,
                data.tanggal_pinjam,
                data.tanggal_kembali,
                data.status,
                data.keterangan
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # DELETE
    # =========================
    def hapus_peminjaman(self, id_peminjaman):
        query = "SELECT hapus_peminjaman(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_peminjaman,))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # PINJAM LAPTOP (BUSINESS LOGIC)
    # =========================
    def pinjam_laptop(self, data: PeminjamanDTO):
        query = """
        SELECT pinjam_laptop(%s,%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_user,
                data.id_laptop_inventori,
                data.id_pengajuan,
                data.tanggal_pinjam,
                data.tanggal_kembali,
                data.keterangan
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # PENGEMBALIAN
    # =========================
    def pengembalian_laptop(self, data: PeminjamanDTO):
        query = """
        SELECT pengembalian_laptop(%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_peminjaman,
                data.lokasi if hasattr(data, "lokasi") else None,
                data.keterangan
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # SYNC STATUS
    # =========================
    def sync_status_laptop(self):
        query = "SELECT sync_status_laptop();"

        with self.conn.cursor() as cur:
            cur.execute(query)
            self.conn.commit()

            return "Status berhasil disinkronkan"

    # =========================
    # LAPTOP BY LOKASI
    # =========================
    def ambil_laptop_by_lokasi(self, data=None):
        query = "SELECT * FROM ambil_laptop_by_lokasi();"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return rows

    # =========================
    # MAPPING DTO
    # =========================
    def _map_to_dto(self, row):
        return PeminjamanDTO(
            id_peminjaman=row.get("id_peminjaman"),
            id_user=row.get("id_user"),
            id_laptop_inventori=row.get("id_laptop_inventori"),
            tanggal_pinjam=row.get("tanggal_pinjam"),
            tanggal_kembali=row.get("tanggal_kembali"),
            status=row.get("status"),
            keterangan=row.get("keterangan")
        )