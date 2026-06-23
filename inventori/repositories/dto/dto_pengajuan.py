class PengajuanDTO:
    def __init__(self,id_pengajuan=None,id_user=None,kebutuhan_role=None,kebutuhan_requirement=None,
                 bulan=None,keterangan=None,perusahaan=None,status=None,tanggal_pengajuan=None,
                 tanggal_approval=None,approved_by=None,id_proyek=None):
        self.id_pengajuan = id_pengajuan
        self.id_user = id_user
        self.kebutuhan_role = kebutuhan_role
        self.kebutuhan_requirement = kebutuhan_requirement
        self.bulan = bulan
        self.keterangan = keterangan
        self.perusahaan = perusahaan
        self.status = status
        self.tanggal_pengajuan= tanggal_pengajuan
        self.tanggal_approval = tanggal_approval
        self.approved_by = approved_by
        self.id_proyek = id_proyek