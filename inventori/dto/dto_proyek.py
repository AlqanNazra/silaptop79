class ProyekDTO:

    def __init__(
        self,
        id_proyek=None,
        nama_proyek=None,
        user_perusahaan=None,
        mulai_proyek=None,
        akhir_proyek=None,
        created_at=None,
        updated_at=None
    ):
        self.id_proyek = id_proyek
        self.nama_proyek = nama_proyek
        self.user_perusahaan = user_perusahaan
        self.mulai_proyek = mulai_proyek
        self.akhir_proyek = akhir_proyek
        self.created_at = created_at
        self.updated_at = updated_at