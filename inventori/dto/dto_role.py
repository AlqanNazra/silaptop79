class RoleDTO:
    def __init__(self, id_role=None, nama_role=None, created_at=None, updated_at=None):
        self.id_role = id_role
        self.nama_role = nama_role
        self.created_at = created_at
        self.updated_at = updated_at

class RoleCriteriaDTO:
    def __init__(self, id_role, nama_role, kriteria_list):
        self.id_role = id_role
        self.nama_role = nama_role
        self.kriteria_list = kriteria_list  # List of dicts berisi bobot kriteria