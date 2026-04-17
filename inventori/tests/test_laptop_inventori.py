import unittest
import psycopg2
from django.test import TransactionTestCase
from django.db import connection
from ..repositories.repositori_laptop_inventori import LaptopInventoriRepository
from ..repositories.dto.dto_laptop_inventori import LaptopInventoriDetailDTO

class TestLaptopInventori(TransactionTestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.conn = psycopg2.connect(
            dbname = "TA",
            user = "postgres",
            password = "alqan",
            host = "127.0.0.1"
        )
        return super().setUpClass()
    
    def setUp(self):
        self.repo = LaptopInventoriRepository(connection)
        self.data_dummy = LaptopInventoriDetailDTO(
        id_laptop_inventori="INV-001",
        no_inventori="LTP-2026-001",
        nama_laptop="Lenovo ThinkPad T14",
        model="ThinkPad T14 Gen 2",
        os="Windows 11 Pro",
        kondisi="Baik",
        status="Tersedia",
        lokasi="Bandung - IT Room",
        ukuran_layar=14.0,
        nama_processor="Intel Core i7",
        manufacturer="Intel",
        processor_model="i7-1165G7",
        cores=4,
        threads=8,
        ram_kapasitas=16,
        ram_tipe="DDR4",
        storage_kapasitas=512,
        storage_tipe="SSD")
        
    def test_tambah_laptop_inventori (self):
        test = self.repo.ambil_laptop_inventori(self.data_dummy)
        self.assertEqual(test, "Berhasil Tambah Alternatif DSS")
        
    def ambil_semua_laptop (self):    
        data = self.repo.ambil_laptop_inventori()
        self.assertIsNone(data)
        
    
        