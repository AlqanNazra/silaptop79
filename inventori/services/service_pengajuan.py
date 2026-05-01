from core.db import get_connection
from inventori.repositories.repositori_pengajuan import PengajuanRepository
from inventori.repositories.dto.dto_pengajuan import PengajuanDTO

class PengajuanService:
    
    def tambah_peminjaman(self, dto: PengajuanDTO):
        conn = get_connection()
        try:
            repo = PengajuanRepository(conn)
            res = repo.tambah_pengajuan(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def hapus_pengajuan(self, id_pengajuan):
        conn = get_connection()
        try:
            repo = PengajuanRepository(conn)
            res = repo.hapus_pengajuan(id_pengajuan)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def ambil_semua_pengajuan(self):
        conn = get_connection()
        try:
            repo = PengajuanRepository(conn)
            res = repo.ambil_semua_pengajuan()
            return res
        finally:
            conn.close()
    
    def cari_pengajuan_by_id(self, id_pengajuan):
        conn = get_connection()
        try:
            repo = PengajuanRepository(conn)
            res = repo.cari_pengajuan(id_pengajuan)
            return res
        finally:
            conn.close()
            
    def approve_pengajuan(self, dto: PengajuanDTO):
        conn = get_connection()
        try:
            repo = PengajuanRepository(conn)
            res = repo.approve_pengajuan(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def approve_dan_pinjam(self, dto_pengajuan, dto_peminjaman):
        conn = get_connection()
        try:
            pengajuan_repo = PengajuanRepository(conn)
            peminjaman_repo = PeminjamanRepository(conn)

            pengajuan_repo.approve_pengajuan(dto_pengajuan)
            peminjaman_repo.pinjam_laptop(dto_peminjaman)

            conn.commit()
        except:
            conn.rollback()
            raise
        finally:
            conn.close()
