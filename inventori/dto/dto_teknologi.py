class TeknologiDTO:

    def __init__(
        self,
        id_teknologi=None,
        nama_teknologi=None,
        kategori=None,
        created_at=None,
        updated_at=None
    ):
        self.id_teknologi = id_teknologi
        self.nama_teknologi = nama_teknologi
        self.kategori = kategori
        self.created_at = created_at
        self.updated_at = updated_at