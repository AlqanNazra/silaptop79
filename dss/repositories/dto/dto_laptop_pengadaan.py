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