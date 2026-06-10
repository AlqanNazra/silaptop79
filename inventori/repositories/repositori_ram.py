import psycopg2
from psycopg2.extras import RealDictCursor
from inventori.dto.dto_ram import RamDTO
from .dto.dto_ram import RamDTO
from .interfaces.interface_ram import IRamRepository


class RamRepository:

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def tambah_ram(self, data: RamDTO):
        query = "SELECT tambah_ram(%s, %s, %s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.kapasitas_gb,
                data.tipe,
                data.keterangan
            ))
            result = cur.fetchone()
            self.conn.commit()

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None

    # =========================
    # READ
    # =========================
    def ambil_ram(self):
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM ambil_ram();")
            return cur.fetchall()
        

    # =========================
    # UPDATE
    # =========================
    def update_ram(self, data: RamDTO):
        query = "SELECT update_ram(%s, %s, %s, %s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_ram,
                data.kapasitas_gb,
                data.tipe,
                data.keterangan
            ))
            result = cur.fetchone()
            self.conn.commit()

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None

    # =========================
    # DELETE
    # =========================
    def hapus_ram(self, id_ram):
        query = "SELECT hapus_ram(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_ram,))
            result = cur.fetchone()
            self.conn.commit()

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None

    # =========================
    # MAPPING
    # =========================
    def _map_to_dto(self, row):
        return RamDTO(
            id_ram=row.get("id_ram"),
            kapasitas_gb=row.get("kapasitas_gb"),
            tipe=row.get("tipe"),
            keterangan=row.get("keterangan")
        )