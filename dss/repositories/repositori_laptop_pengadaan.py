import psycopg2
from psycopg2.extras import RealDictCursor
from dto.dto_laptop_pengadaan import LaptopPengadaanDTO
from interface.interface_laptop_pengadaan import ILaptopPengadaanRepositoryImpl


class LaptopPengadaanRepository(ILaptopPengadaanRepositoryImpl):

    def __init__(self, conn):
        self.conn = conn

    def tambah_laptop_pengadaan(self, data: LaptopPengadaanDTO):
        query = """
        SELECT tambah_laptop_pengadaan(%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.nama_laptop,
                data.harga,
                data.gpu,
                data.ukuran_layar,
                data.baterai,
                data.id_processor,
                data.id_ram,
                data.id_storage,
                data.berat
            ))
            self.conn.commit()

            return "Berhasil tambah laptop pengadaan"

    def ambil_laptop_pengadaan(self):
        query = "SELECT * FROM ambil_laptop_pengadaan();"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

            return rows  
        
    def update_laptop_pengadaan(self, data: LaptopPengadaanDTO):
        query = """
        SELECT update_laptop_pengadaan(%s,%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_laptop_pengadaan,
                data.nama_laptop,
                data.harga,
                data.gpu,
                data.ukuran_layar,
                data.baterai
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None
        
    def update_spek_pengadaan(self, data: LaptopPengadaanDTO):
        query = """
        SELECT update_spek_pengadaan(%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_laptop_pengadaan,
                data.id_processor,
                data.id_ram,
                data.id_storage
            ))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None
        
    def hapus_laptop_pengadaan(self, id_laptop_pengadaan):
        query = "SELECT hapus_laptop_pengadaan(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_laptop_pengadaan,))
            result = cur.fetchone()
            self.conn.commit()

            return result[0] if result else None
        
    def ambil_hasil_saw_pengadaan(self, id_hasil):
        query = "SELECT * FROM ambil_hasil_saw_pengadaan(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_hasil,))
            rows = cur.fetchall()

            return rows
        
    def filter_pengadaan(self, filter_dto: LaptopPengadaanDTO) -> list:
        query = """
            SELECT * FROM GetFilteredLaptopPengadaan(
                %s,                            -- id_laptop_pengadaan
                %s, %s, %s,                    -- harga, min_harga, max_harga
                %s,                            -- gpu
                %s, %s, %s,                    -- ukuran_layar, min, max
                %s, %s, %s,                    -- baterai, min, max
                %s, %s, %s,                    -- nama_processor, manufacturer, processor_model
                %s, %s, %s,                    -- cores, min_cores, max_cores
                %s, %s, %s, %s,                -- ram_kapasitas, min, max, tipe
                %s, %s, %s, %s                 -- storage_kapasitas, min, max, tipe
            );
        """

        params = filter_dto.get_params()

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            return [self._map_to_dto(row) for row in rows]
