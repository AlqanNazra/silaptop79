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