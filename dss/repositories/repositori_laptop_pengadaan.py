from tkinter import END

import psycopg2
from psycopg2.extras import RealDictCursor
from .dto.dto_laptop_pengadaan import LaptopPengadaanDTO
from .interface.interface_laptop_pengadaan import ILaptopPengadaanRepositoryImpl


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

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None
        
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

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None
        
    def hapus_laptop_pengadaan(self, id_laptop_pengadaan):
        query = "SELECT hapus_laptop_pengadaan(%s);"

        with self.conn.cursor() as cur:
            cur.execute(query, (id_laptop_pengadaan,))
            result = cur.fetchone()
            self.conn.commit()

            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None
        
    def ambil_hasil_saw_pengadaan(self, id_hasil):
        query = "SELECT * FROM ambil_hasil_saw_pengadaan(%s);"

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (id_hasil,))
            rows = cur.fetchall()

            return rows
        
    def filter_pengadaan(self, filter_dto):
        query = """
            SELECT * FROM GetFilteredLaptopPengadaan(
                %s,
                %s, %s, %s,
                %s,
                %s, %s, %s,
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
            return cur.fetchall()

    def ambil_laptop_pengadaan_by_id(self, id_laptop_pengadaan):
        # Menggunakan triple quotes untuk multiline string
        query = """
        SELECT 
            lp.id_laptop_pengadaan,
            lp.nama_laptop,
            lp.harga,
            lp.gpu,
            lp.ukuran_layar,
            lp.baterai,
            lp.berat,
            pro.nama_processor,
            pro.manufacturer,
            pro.model AS processor_model,
            pro.cores,
            pro.threads,
            pro.processor_score,
            r.kapasitas_gb AS ram_kapasitas,
            r.tipe AS ram_tipe,
            s.kapasitas_gb AS storage_kapasitas,
            s.tipe AS storage_tipe
        FROM dss_laptoppengadaan lp
        LEFT JOIN inventori_processor pro ON lp.processor_id = pro.id_processor
        LEFT JOIN inventori_ram r ON lp.ram_id = r.id_ram
        LEFT JOIN inventori_storage s ON lp.storage_id = s.id_storage
        WHERE lp.id_laptop_pengadaan = %s;  -- <--- PENTING: Tambahkan ini untuk memfilter berdasarkan ID
        """
        
        params = (id_laptop_pengadaan,)

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            row = cur.fetchone()  # Menggunakan fetchone() karena hasilnya pasti cuma 1 data (atau None)
            return row