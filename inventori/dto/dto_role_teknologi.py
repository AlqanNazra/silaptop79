
from datetime import datetime

class RoleTeknologiDTO:
     def __init__(self, id_role_teknologi = None, id_role = None, id_teknologi = None, nama_role = None
                 ,nama_teknologi = None, is_default = None, created_at = None):
        self.id_role_teknologi = id_role_teknologi
        self.id_role = id_role
        self.id_teknologi = id_teknologi
        self.nama_role = nama_role
        self.nama_teknologi = nama_teknologi
        self.is_default: bool = is_default
        self.created_at: datetime = created_at