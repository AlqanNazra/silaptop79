class LaptopInventoriDetailDTO:
    def __init__(self,
                 id_laptop_inventori=None,no_inventori=None,nama_laptop=None,model=None,os=None,kondisi=None,
                 status=None,lokasi=None,ukuran_layar=None,nama_processor=None,manufacturer=None,
                 processor_model=None,cores=None,threads=None,ram_kapasitas=None,ram_tipe=None,
                 storage_kapasitas=None,storage_tipe=None):
        
        self.id_laptop_inventori = id_laptop_inventori
        self.no_inventori = no_inventori
        self.nama_laptop = nama_laptop
        self.model = model
        self.os = os
        self.kondisi = kondisi
        self.status = status
        self.lokasi = lokasi
        self.ukuran_layar = ukuran_layar
        self.nama_processor = nama_processor
        self.manufacturer = manufacturer
        self.processor_model = processor_model
        self.cores = cores
        self.threads = threads
        self.ram_kapasitas = ram_kapasitas
        self.ram_tipe = ram_tipe
        self.storage_kapasitas = storage_kapasitas
        self.storage_tipe = storage_tipe
        
        
class FilterInventoriDTO:
    """DTO untuk parameter filter laptop inventori"""

    def __init__(
        self,
        id_laptop_inventori: str = None,
        kondisi: str = None,
        status: str = None,
        lokasi: str = None,
        ukuran_layar: float = None,
        min_ukuran_layar: float = None,
        max_ukuran_layar: float = None,
        nama_processor: str = None,
        manufacturer: str = None,
        processor_model: str = None,
        cores: int = None,
        min_cores: int = None,
        max_cores: int = None,
        ram_kapasitas: int = None,
        min_ram_kapasitas: int = None,
        max_ram_kapasitas: int = None,
        ram_tipe: str = None,
        storage_kapasitas: int = None,
        min_storage: int = None,
        max_storage: int = None,
        storage_tipe: str = None
    ):
        self.id_laptop_inventori = id_laptop_inventori
        self.kondisi = kondisi
        self.status = status
        self.lokasi = lokasi
        self.ukuran_layar = ukuran_layar
        self.min_ukuran_layar = min_ukuran_layar
        self.max_ukuran_layar = max_ukuran_layar
        self.nama_processor = nama_processor
        self.manufacturer = manufacturer
        self.processor_model = processor_model
        self.cores = cores
        self.min_cores = min_cores
        self.max_cores = max_cores
        self.ram_kapasitas = ram_kapasitas
        self.min_ram_kapasitas = min_ram_kapasitas
        self.max_ram_kapasitas = max_ram_kapasitas
        self.ram_tipe = ram_tipe
        self.storage_kapasitas = storage_kapasitas
        self.min_storage = min_storage
        self.max_storage = max_storage
        self.storage_tipe = storage_tipe
        
    def get_params(self) -> tuple:
        """Mengembalikan parameter dalam bentuk tuple sesuai urutan function SQL"""
        return (
            self.id_laptop_inventori,
            self.kondisi,
            self.status,
            self.lokasi,
            self.ukuran_layar,
            self.min_ukuran_layar,
            self.max_ukuran_layar,
            self.nama_processor,
            self.manufacturer,
            self.processor_model,
            self.cores,
            self.min_cores,
            self.max_cores,
            self.ram_kapasitas,
            self.min_ram_kapasitas,
            self.max_ram_kapasitas,
            self.ram_tipe,
            self.storage_kapasitas,
            self.min_storage,
            self.max_storage,
            self.storage_tipe,
            self.min_ram_kapasitas,
            self.min_storage
        )

# Alias sederhana yang dipakai oleh views.py untuk operasi CRUD input
class LaptopInventoriDTO:
    def __init__(self, id_laptop_inventori=None, no_inventori=None, nama_laptop=None,
                 model=None, os=None, kondisi=None, status=None, lokasi=None,
                 id_processor=None, id_ram=None, id_storage=None, ukuran_layar=None, baterai=None):
        self.id_laptop_inventori = id_laptop_inventori
        self.no_inventori = no_inventori
        self.nama_laptop = nama_laptop
        self.model = model
        self.os = os
        self.kondisi = kondisi
        self.status = status
        self.lokasi = lokasi
        self.id_processor = id_processor
        self.id_ram = id_ram
        self.id_storage = id_storage
        self.ukuran_layar = ukuran_layar
        self.baterai = baterai