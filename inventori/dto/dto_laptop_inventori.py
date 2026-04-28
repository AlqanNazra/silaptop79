class LaptopInventoriDTO:
    def __init__(self, id_laptop_inventori=None, no_inventori=None, nama_laptop=None, 
                 model=None, os=None, kondisi=None, status=None, lokasi=None, 
                 id_processor=None, id_ram=None, id_storage=None, ukuran_layar=None):
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
