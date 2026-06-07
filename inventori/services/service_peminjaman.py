from core.db import get_connection
from inventori.repositories.repositori_peminjaman import PeminjamanRepository
from inventori.repositories.dto.dto_peminjaman import PeminjamanDTO

class PeminjamanService:
    
    def service_tambah_peminjaman(self, dto: PeminjamanDTO):
        conn = get_connection()
        try:
            repo = PeminjamanRepository(conn)
            res = repo.tambah_peminjaman(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def service_hapus_peminjaman(self, id_peminjaman):
        conn = get_connection()
        try:
            repo = PeminjamanRepository(conn)
            res = repo.hapus_peminjaman(id_peminjaman)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def service_ambil_semua_peminjaamn(self):
        conn = get_connection()
        try:
            repo = PeminjamanRepository(conn)
            res = repo.ambil_semua_peminjaman()
            return res
        finally:
            conn.close()
            
    def service_ambil_semua_peminjaman(self):
        return self.service_ambil_semua_peminjaamn()
            
    def service_cari_peminjaman(self,id_peminjaman):
        conn = get_connection()
        try:
            repo = PeminjamanRepository(conn)
            res = repo.cari_peminjaman(id_peminjaman)
            return res
        finally:
            conn.close()
            
    def service_ambil_laptop_by_lokasi(self):
        conn = get_connection()
        try:
            repo = PeminjamanRepository(conn)
            res = repo.ambil_laptop_by_lokasi()
            return res
        finally:
            conn.close()

    def service_update_peminjaman(self, dto: PeminjamanDTO):
        conn = get_connection()
        try:
            repo = PeminjamanRepository(conn)
            res = repo.update_peminjaman(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            
    def service_pinjam_laptop(self, dto: PeminjamanDTO):
        conn = get_connection()
        try:
            repo = PeminjamanRepository(conn)
            res = repo.pinjam_laptop(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def service_pengembalian_laptop(self, dto: PeminjamanDTO):
        conn = get_connection()
        try:
            repo = PeminjamanRepository(conn)
            res = repo.pengembalian_laptop(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def service_sync_status_laptop(self):
        conn = get_connection()
        try:
            repo = PeminjamanRepository(conn)
            res = repo.sync_status_laptop()
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
