from ..repositories.dto.dto_dss_proses import DssProsesDTO
from ..repositories.dto.dto_alternatif_dss import AlternatifDssDTO
from ..repositories.interface.interface_dss_proses import IDssProssesRepositoryImpl
from ..repositories.interface.interface_alternatif_dss import IAlternatifDssImpl

class DssProsesService:

    def __init__(
        self,
        dss_repo: IDssProssesRepositoryImpl,
        alternatif_repo: IAlternatifDssImpl
    ):
        self.dss_repo = dss_repo
        self.alternatif_repo = alternatif_repo

    def buat_proses_dss(self, data: DssProsesDTO):
        if not data.id_user:
            raise ValueError("ID User wajib diisi")

        if not data.role_dss:
            raise ValueError("Role DSS wajib diisi")

        return self.dss_repo.tambah_dss_proses(data)

    def tambah_alternatif(self, data: AlternatifDssDTO):
        if not data.id_dss:
            raise ValueError("ID DSS wajib ada")

        if not data.id_alternatif:
            raise ValueError("ID Alternatif wajib ada")

        return self.alternatif_repo.tambah_alternatif_dss(data)
    def proses_dss_lengkap(self, dss_data: DssProsesDTO, list_alternatif: map[AlternatifDssDTO]):
        """
        Alur:
        1. Buat proses DSS
        2. Tambahkan semua alternatif ke DSS
        """
        hasil_dss = self.buat_proses_dss(dss_data)
        id_dss = dss_data.id_dss
        hasil_alternatif = []
        for alt in list_alternatif:
            alt.id_dss = id_dss
            res = self.tambah_alternatif(alt)
            hasil_alternatif.append(res)

        return {
            "dss": hasil_dss,
            "alternatif": hasil_alternatif
        }
        
    def get_semua_dss(self):
        return self.dss_repo.ambil_semua_dss_proses()
    
    def cari_alternatif(self, id_alternatif):
        return self.alternatif_repo.cari_alternatif_dss(id_alternatif)

    def hapus_alternatif(self, id_alternatif):
        return self.alternatif_repo.hapus_alternatif_dss(id_alternatif)