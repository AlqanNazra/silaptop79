class RoleDTO:
    def __init__(
        self,
        id_role=None,
        nama_role=None,
        min_ram=0,
        min_storage=0,
        nama_processor=None,
        min_processor_score=0,
        created_at=None,
        updated_at=None
    ):
        self.id_role = id_role
        self.nama_role = nama_role
        self.min_ram = min_ram
        self.min_storage = min_storage
        self.nama_processor = nama_processor
        self.min_processor_score = min_processor_score
        self.created_at = created_at
        self.updated_at = updated_at
class RoleCriteriaDTO:
    def __init__(self, id_role, nama_role, kriteria_list):
        
        self.id_role = id_role
        self.nama_role = nama_role
        self.kriteria_list = kriteria_list  # List of dicts berisi bobot kriteria