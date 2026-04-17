class AlternatifDssDTO:
    def __init__(self,id_alternatif=None,id_dss=None,id_laptop_pengadaan=None,
                 id_laptop_inventori=None,sumber_data=None):
        self.id_alternatif=id_alternatif
        self.id_dss=id_dss
        self.id_laptop_pengadaan=id_laptop_pengadaan
        self.id_laptop_inventori=id_laptop_inventori
        self.sumber_data=sumber_data