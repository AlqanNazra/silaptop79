import psycopg2
from psycopg2.extras import RealDictCursor
from inventori.dto.dto_riwayat_aktivitas import RiwayatAktivitasDTO


class RiwayatAktivitasRepository:

    def __init__(self, conn):
        self.conn = conn

    def create_riwayat(self, dto: RiwayatAktivitasDTO):
        query = """
        SELECT create_riwayat_aktivitas(%s, %s, %s, %s, %s, %s);
        """
        with self.conn.cursor() as cur:
            cur.execute(query, [
                dto.id_user,
                dto.id_laptop,
                dto.nama_aset,
                dto.role_pengguna,
                dto.jenis_aktivitas,
                dto.keterangan
            ])
            self.conn.commit()

    def ambil_semua_riwayat(self):
        query = "SELECT * FROM get_all_riwayat();"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return [self._map_to_dto(row) for row in rows]

    def ambil_cari_riwayat(self, id_aktivitas):
        query = """
        SELECT * FROM get_all_riwayat()
        WHERE id_aktivitas = %s;
        """
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_aktivitas,))
            row = cur.fetchone()
            return self._map_to_dto(row) if row else None

    def ambil_cari_riwayat_laptop(self, id_laptop):
        query = "SELECT * FROM get_riwayat_by_laptop(%s);"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_laptop,))
            rows = cur.fetchall()
            return rows  # karena struktur berbeda (tidak full DTO)

    def ambil_cari_riwayat_user(self, id_user):
        query = "SELECT * FROM get_riwayat_by_user(%s);"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_user,))
            rows = cur.fetchall()
            return rows

    def ambil_cari_riwayat_jenis(self, jenis):
        query = "SELECT * FROM get_riwayat_by_jenis(%s);"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (jenis,))
            rows = cur.fetchall()
            return rows
        
    def ambil_cari_riwayat_tanggal(self, tanggal):
        query = "SELECT * FROM get_riwayat_by_tanggal(%s);"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (tanggal,))
            rows = cur.fetchall()
            return rows
        
    def ambil_cari_riwayat_filter_riwayat(self, id_laptop, id_user, tanggal, jenis):
        query = "SELECT * FROM filter_riwayat(%s, %s, %s, %s);"
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_laptop, id_user, tanggal, jenis))
            rows = cur.fetchall()
            return [self._map_to_dto(row) for row in rows]

    def hapus_riwayat_aktivitas(self, id_aktivitas):
        query = "SELECT delete_riwayat(%s);"
        with self.conn.cursor() as cur:
            cur.execute(query, (id_aktivitas,))
            result = cur.fetchone()
            self.conn.commit()
            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None
        
    def _map_to_dto(self, row):
        if not row:
            return None

        return RiwayatAktivitasDTO(
            id_aktivitas=row.get("id_aktivitas"),
            id_user=row.get("id_user"),
            id_laptop=row.get("id_laptop"),
            jenis_aktivitas=row.get("jenis_aktivitas"),
            keterangan=row.get("keterangan")
        )