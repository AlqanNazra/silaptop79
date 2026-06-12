class BobotKriteriaDTO:
    def __init__(self,
                 id_bobot=None,id_kriteria=None,role=None,
                 nilai_bobot=None,nilai_swara = None,versi = None,
                 is_active= None,created_at= None,id_role_teknologi= None):
        self.id_bobot=id_bobot
        self.id_kriteria=id_kriteria
        self.role = role
        self.nilai_bobot=nilai_bobot
        self.nilai_swara = nilai_swara
        self.versi = versi
        self.is_active = is_active
        self.created_at = created_at
        self.id_role_teknologi = id_role_teknologi