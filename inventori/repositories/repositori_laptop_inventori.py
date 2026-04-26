import psycopg2
from psycopg2.extras import RealDictCursor
from dto.dto_laptop_inventori import LaptopInventoriDetailDTO
from interfaces.interface_laptop_inventori import ILaptopInventoriRepository


class LaptopInventoriRepository(ILaptopInventoriRepository):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def tambah_laptop_inventori(self, data: LaptopInventoriDetailDTO):
        query = """
        SELECT tambah_laptop_inventori(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.nama_laptop,
                data.model,
                data.os,
                data.kondisi,
                data.status,
                data.lokasi,
                data.id_processor,
                data.id_ram,
                data.id_storage,
                data.ukuran_layar
            ))
            self.conn.commit()

            return "Berhasil tambah laptop inventori"

    # =========================
    # READ DETAIL SPEK
    # =========================
    def ambil_spek_laptop(self, id_laptop_inventori):
        query = "SELECT * FROM ambil_spek_laptop(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_laptop_inventori,))
            return cur.fetchone()

    # =========================
    # READ ALL INVENTORI
    # =========================
    def ambil_laptop_inventori(self):
        query = "SELECT * FROM ambil_laptop_inventori();"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return [self._map_to_detail_dto(row) for row in rows]

    # =========================
    # HASIL DSS SAW
    # =========================
    def ambil_hasil_saw_inventori(self, id_hasil):
        query = "SELECT * FROM ambil_hasil_saw_inventori(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_hasil,))
            rows = cur.fetchall()

            return rows

    # =========================
    # UPDATE KONDISI
    # =========================
    def update_kondisi_inventori(self, id_laptop_inventori, kondisi):
        query = "SELECT update_kondisi_inventori(%s,%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_laptop_inventori, kondisi))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # DELETE
    # =========================
    def hapus_laptop_inventori(self, id_laptop_inventori):
        query = "SELECT hapus_laptop_inventori(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_laptop_inventori,))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None

    # =========================
    # UPDATE SPEK
    # =========================
    def update_spek_inventori(self, id_laptop_inventori, id_processor, id_ram, id_storage):
        query = "SELECT update_spek_inventori(%s,%s,%s,%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (
                id_laptop_inventori,
                id_processor,
                id_ram,
                id_storage
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None
        
    def _map_to_detail_dto(self, row):
        return LaptopInventoriDetailDTO(
            id_laptop_inventori=row.get("id_laptop_inventori"),
            no_inventori=row.get("no_inventori"),
            nama_laptop=row.get("nama_laptop"),
            model=row.get("model"),
            os=row.get("os"),
            kondisi=row.get("kondisi"),
            status=row.get("status"),
            lokasi=row.get("lokasi"),
            ukuran_layar=row.get("ukuran_layar"),

            nama_processor=row.get("nama_processor"),
            manufacturer=row.get("manufacturer"),
            processor_model=row.get("processor_model"),
            cores=row.get("cores"),
            threads=row.get("threads"),

            ram_kapasitas=row.get("ram_kapasitas"),
            ram_tipe=row.get("ram_tipe"),

            storage_kapasitas=row.get("storage_kapasitas"),
            storage_tipe=row.get("storage_tipe")
        )
        
    def filter_inventori(self, data: LaptopInventoriDetailDTO) -> list:
        query = """
            SELECT * FROM GetFilteredLaptopInventori(
                %s, %s, %s, %s,               -- id, kondisi, status, lokasi
                %s, %s, %s,                   -- ukuran_layar, min, max
                %s, %s, %s,                   -- nama_processor, manufacturer, processor_model
                %s, %s, %s,                   -- cores, min_cores, max_cores
                %s, %s, %s, %s,               -- ram_kapasitas, min, max, tipe
                %s, %s, %s, %s                -- storage_kapasitas, min, max, tipe
            );
        """

        params = data.get_params()

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return [self._map_to_dto(row) for row in rows]