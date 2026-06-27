from inventori.repositories.interfaces.interface_laptop_inventori import ILaptopInventoriRepository
from psycopg2.extras import RealDictCursor

class LaptopInventoriRepository(ILaptopInventoriRepository):
    def __init__(self, connection):
        self.conn = connection

    def tambah_laptop(self, dto):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT tambah_laptop_inventori(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (dto.nama_laptop, dto.model, dto.os, dto.kondisi, dto.status, 
                  dto.lokasi, dto.id_processor, dto.id_ram, dto.id_storage, dto.ukuran_layar, dto.baterai))
            return cur.fetchone()['tambah_laptop_inventori']


    def ambil_laptop(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM ambil_laptop_inventori()")
            rows = cur.fetchall()
            for r in rows:
                if r.get('berat') is None:
                    r['berat'] = 0
                if r.get('baterai') is None:
                    r['baterai'] = 0
                if r.get('benchmark_score') is None:
                    r['benchmark_score'] = 0
                if r.get('ukuran_layar') is None:
                    r['ukuran_layar'] = 0
            return rows

    def ambil_spek_laptop(self,id_laptop):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""SELECT *FROM ambil_spek_laptop(%s)""",(id_laptop,))
            return cur.fetchone()

    def update_kondisi(self, id_laptop, kondisi):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT update_kondisi_inventori(%s, %s)", (id_laptop, kondisi))
            res = cur.fetchone()
            return res.get('update_kondisi_inventori') if res else None

    def update_status(self, id_laptop, status, lokasi):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT update_status_inventori(%s, %s, %s)", (id_laptop, status, lokasi))
            res = cur.fetchone()
            return res.get('update_status_inventori') if res else None

    def update_spek(self, dto):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT update_spek_inventori(%s, %s, %s, %s)
            """, (dto.id_laptop_inventori, dto.id_processor, dto.id_ram, dto.id_storage))
            res = cur.fetchone()
            return res.get('update_spek_inventori') if res else None

    def hapus_laptop(self, id_laptop):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT hapus_laptop_inventori(%s)", (id_laptop,))
            res = cur.fetchone()
            return res.get('hapus_laptop_inventori') if res else None

    def filter_inventori(self, filter_dto):
        query = """
            SELECT * FROM GetFilteredLaptopinventori(
                %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,%s
            );
        """

        params = filter_dto.get_params()

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            
            try:
                cur.execute("SELECT id_laptop_inventori FROM inventori_peminjaman WHERE status IN ('dipinjam', 'ready', 'aktif');")
                active_loans = {r['id_laptop_inventori'] for r in cur.fetchall() if r.get('id_laptop_inventori')}
            except Exception:
                active_loans = set()

            filtered_rows = []
            for r in rows:
                if r.get('berat') is None:
                    r['berat'] = 0
                if r.get('baterai') is None:
                    r['baterai'] = 0
                if r.get('benchmark_score') is None:
                    r['benchmark_score'] = 0
                if r.get('ukuran_layar') is None:
                    r['ukuran_layar'] = 0
                
                lap_id = r.get('id_laptop_inventori')
                st = str(r.get('status', '')).lower()
                kd = str(r.get('kondisi', '')).lower()
                
                if lap_id in active_loans or st in ['dipinjam', 'rusak', 'perbaikan'] or kd in ['rusak', 'rusak berat']:
                    continue
                filtered_rows.append(r)
            return filtered_rows
        
    def ambil_detail_laptop(self, id_laptop):
        query = """
        SELECT *
        FROM ambil_detail_laptop_inventori(%s)
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(query, (id_laptop,))
            return cur.fetchone()