from ..repositories.dto.dto_hasil_saw import HasilSAWDTO
from ..repositories.dto.dto_detail_hasil_saw import DetailHasilSawDTO
from ..repositories.interface.interface_hasil_saw import IHasilSawRepositoryImpl
from ..repositories.interface.interface_detail_hasil_saw import IDetailHasilSawImpl

class HasilSawService:

    def __init__(
        self,
        hasil_repo: IHasilSawRepositoryImpl,
        detail_repo: IDetailHasilSawImpl,
        conn  # penting untuk transaksi
    ):
        self.hasil_repo = hasil_repo
        self.detail_repo = detail_repo
        self.conn = conn

    # =====================================
    # 1. BUAT HASIL SAW (HEADER)
    # =====================================
    def buat_hasil(self, data: HasilSAWDTO):
        if not data.id_dss:
            raise ValueError("ID DSS wajib diisi")

        return self.hasil_repo.buat_hasil_saw(data)

    # =====================================
    # 2. TAMBAH DETAIL
    # =====================================
    def tambah_detail(self, data: DetailHasilSawDTO):
        if not data.id_hasil:
            raise ValueError("ID Hasil wajib ada")

        return self.detail_repo.tambah_detail_hasil_saw(data)

    # =====================================
    # 3. PROSES LENGKAP SAW (ORCHESTRATION)
    # =====================================
    def proses_saw_lengkap(self, hasil_data: HasilSAWDTO, list_detail: list[DetailHasilSawDTO]):
        """
        Alur:
        1. Buat hasil SAW
        2. Simpan semua detail ranking
        """

        try:
            # =====================
            # 1. Buat header hasil
            # =====================
            hasil = self.buat_hasil(hasil_data)

            # ⚠️ idealnya ambil id_hasil dari DB
            id_hasil = hasil_data.id_hasil

            # =====================
            # 2. Simpan detail
            # =====================
            hasil_detail = []

            for detail in list_detail:
                detail.id_hasil = id_hasil
                res = self.tambah_detail(detail)
                hasil_detail.append(res)

            # =====================
            # COMMIT SEKALI SAJA
            # =====================
            self.conn.commit()

            return {
                "hasil": hasil,
                "detail": hasil_detail
            }

        except Exception as e:
            # rollback kalau gagal
            self.conn.rollback()
            raise e

    # =====================================
    # 4. AMBIL DETAIL BY ID
    # =====================================
    def get_detail_by_id(self, id_detail):
        return self.detail_repo.cari_data_detail_hasil_saw(id_detail)

    # =====================================
    # 5. AMBIL SEMUA DETAIL
    # =====================================
    def get_all_detail(self):
        return self.detail_repo.ambil_semua_data_detail_hasil_saw()

    # =====================================
    # 6. HAPUS DETAIL
    # =====================================
    def hapus_detail(self, id_detail):
        return self.detail_repo.hapus_detail_hasil_saw(id_detail)