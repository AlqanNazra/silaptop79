from inventori.repositories.interfaces.interface_laptop_inventori import ILaptopInventoriRepository
from psycopg2.extras import RealDictCursor

class LaptopInventoriRepository(ILaptopInventoriRepository):
    def __init__(self, connection):
        self.conn = connection

    def tambah_laptop(self, dto):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT tambah_laptop_inventori(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (dto.nama_laptop, dto.model, dto.os, dto.kondisi, dto.status, 
                  dto.lokasi, dto.id_processor, dto.id_ram, dto.id_storage, dto.ukuran_layar))
            return cur.fetchone()['tambah_laptop_inventori']


    def ambil_laptop(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM ambil_laptop_inventori()")
            return cur.fetchall()

    def ambil_spek_laptop(self, id_laptop):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM ambil_spek_laptop(%s)", (id_laptop,))
            return cur.fetchone()

    def update_kondisi(self, id_laptop, kondisi):
        with self.conn.cursor() as cur:
            cur.execute("SELECT update_kondisi_inventori(%s, %s)", (id_laptop, kondisi))
            return cur.fetchone()['update_kondisi_inventori']

    def update_status(self, id_laptop, status, lokasi):
        with self.conn.cursor() as cur:
            cur.execute("SELECT update_status_inventori(%s, %s, %s)", (id_laptop, status, lokasi))
            return cur.fetchone()['update_status_inventori']

    def update_spek(self, dto):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT update_spek_inventori(%s, %s, %s, %s)
            """, (dto.id_laptop_inventori, dto.id_processor, dto.id_ram, dto.id_storage))
            return cur.fetchone()['update_spek_inventori']

    def hapus_laptop(self, id_laptop):
        with self.conn.cursor() as cur:
            cur.execute("SELECT hapus_laptop_inventori(%s)", (id_laptop,))
            return cur.fetchone()['hapus_laptop_inventori']

    def filter_inventori(self, filter_dto):
        query = """
            SELECT * FROM GetFilteredLaptopinventori(
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s
            );
        """

        params = filter_dto.get_params()

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()