import psycopg2
from psycopg2.extras import RealDictCursor
from inventori.dto.dto_pengajuan import PengajuanDTO
from .dto.dto_pengajuan import PengajuanDTO
from .interfaces.interface_pengajuan import IPengajuanRepository



class PengajuanRepository:

    def __init__(self, conn):
        self.conn = conn

    def tambah_pengajuan(self, data: PengajuanDTO):
        query = """
        SELECT tambah_pengajuan(%s,%s,%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_user,
                data.kebutuhan_role,
                data.kebutuhan_requirement,
                data.bulan,
                data.keterangan,
                data.perusahaan,
                data.id_proyek
            ))
            self.conn.commit()

            return "Pengajuan berhasil ditambahkan"

    def ambil_semua_pengajuan(self):
        query = "SELECT * FROM ambil_semua_pengajuan();"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [self._map_to_dto(row) for row in rows]

    def cari_pengajuan(self, id_pengajuan):
        query = "SELECT * FROM cari_pengajuan(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_pengajuan,))
            row = cur.fetchone()
            return self._map_to_dto(row) if row else None

    def hapus_pengajuan(self, id_pengajuan):
        query = "SELECT hapus_pengajuan(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_pengajuan,))
            result = cur.fetchone()
            self.conn.commit()
            # Use safe dict/tuple retrieval to avoid KeyError/IndexError
            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None

    def approve_pengajuan(self, data: PengajuanDTO):
        query = """
        SELECT approve_pengajuan(%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_pengajuan,
                data.status,        # approved / rejected
                data.approved_by
            ))
            result = cur.fetchone()
            self.conn.commit()
            # Use safe dict/tuple retrieval to avoid KeyError/IndexError
            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None

    def _map_to_dto(self, row):
        return PengajuanDTO(
            id_pengajuan=row.get("id_pengajuan"),
            id_user=row.get("id_user"),
            kebutuhan_role=row.get("kebutuhan_role"),
            kebutuhan_requirement=row.get("kebutuhan_requirement"),
            bulan=row.get("bulan"),
            keterangan=row.get("keterangan"),
            perusahaan=row.get("perusahaan"),
            status=row.get("status"),
            tanggal_pengajuan=row.get("tanggal_pengajuan"),
            tanggal_approval=row.get("tanggal_approval"),
            approved_by=row.get("approved_by"),
            id_proyek=row.get("id_proyek")
        )