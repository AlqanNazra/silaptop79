class LaptopPengadaanDTO:
    def __init__(self,id_laptop_pengadaan=None,id_processor=None,id_ram=None,id_storage=None,nama_laptop=None,
                 harga=None,gpu=None,ukuran_layar=None,baterai=None,berat=None):
        self.id_laptop_pengadaan=id_laptop_pengadaan
        self.id_processor=id_processor
        self.id_ram=id_ram
        self.id_storage=id_storage
        self.nama_laptop=nama_laptop
        self.harga=harga
        self.gpu=gpu
        self.ukuran_layar=ukuran_layar
        self.baterai=baterai
        self.berat=berat
        
class FilterPengadaanDTO:
    def __init__(
        self,
        id_laptop_pengadaan: str = None,
        harga: float = None,
        min_harga: float = None,
        max_harga: float = None,
        gpu: str = None,
        ukuran_layar: float = None,
        min_ukuran_layar: float = None,
        max_ukuran_layar: float = None,
        baterai: float = None,
        min_baterai: float = None,
        max_baterai: float = None,
        nama_processor: str = None,
        manufacturer: str = None,
        processor_model: str = None,
        processor_score: int = None,
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
        self.id_laptop_pengadaan = id_laptop_pengadaan
        self.harga = harga
        self.min_harga = min_harga
        self.max_harga = max_harga
        self.gpu = gpu
        self.ukuran_layar = ukuran_layar
        self.min_ukuran_layar = min_ukuran_layar
        self.max_ukuran_layar = max_ukuran_layar
        self.baterai = baterai
        self.min_baterai = min_baterai
        self.max_baterai = max_baterai
        self.nama_processor = nama_processor
        self.manufacturer = manufacturer
        self.processor_model = processor_model
        self.processor_score = processor_score
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
        return (
            self.id_laptop_pengadaan,
            self.harga,
            self.min_harga,
            self.max_harga,
            self.gpu,
            self.ukuran_layar,
            self.min_ukuran_layar,
            self.max_ukuran_layar,
            self.baterai,
            self.min_baterai,
            self.max_baterai,
            self.nama_processor,
            self.manufacturer,
            self.processor_model,
            self.processor_score,
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
            self.storage_tipe
        )