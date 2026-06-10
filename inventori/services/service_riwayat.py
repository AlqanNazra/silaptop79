from core.db import get_connection
from inventori.repositories.repositori_riwayat_laptop import RiwayatAktivitasRepository
from inventori.repositories.dto.dto_riwayat_aktivitas import RiwayatAktivitasDTO


class RiwayatAktivitasService:

    # CREATE
    def service_create_riwayat(self, dto: RiwayatAktivitasDTO):
        conn = get_connection()
        try:
            repo = RiwayatAktivitasRepository(conn)
            res = repo.create_riwayat(dto)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    # READ ALL
    def service_ambil_semua_riwayat(self):
        conn = get_connection()
        try:
            repo = RiwayatAktivitasRepository(conn)
            res = repo.ambil_semua_riwayat()
            return res
        finally:
            conn.close()

    # READ BY ID
    def service_ambil_riwayat_by_id(self, id_aktivitas):
        conn = get_connection()
        try:
            repo = RiwayatAktivitasRepository(conn)
            res = repo.ambil_cari_riwayat(id_aktivitas)
            return res
        finally:
            conn.close()

    # FILTER BY LAPTOP
    def service_ambil_riwayat_by_laptop(self, id_laptop):
        conn = get_connection()
        try:
            repo = RiwayatAktivitasRepository(conn)
            res = repo.ambil_cari_riwayat_laptop(id_laptop)
            return res
        finally:
            conn.close()

    # FILTER BY USER
    def service_ambil_riwayat_by_user(self, id_user):
        conn = get_connection()
        try:
            repo = RiwayatAktivitasRepository(conn)
            res = repo.ambil_cari_riwayat_user(id_user)
            return res
        finally:
            conn.close()

    # FILTER BY JENIS
    def service_ambil_riwayat_by_jenis(self, jenis):
        conn = get_connection()
        try:
            repo = RiwayatAktivitasRepository(conn)
            res = repo.ambil_cari_riwayat_jenis(jenis)
            return res
        finally:
            conn.close()

    # FILTER BY TANGGAL
    def service_ambil_riwayat_by_tanggal(self, tanggal):
        conn = get_connection()
        try:
            repo = RiwayatAktivitasRepository(conn)
            res = repo.ambil_cari_riwayat_tanggal(tanggal)
            return res
        finally:
            conn.close()

    # FILTER KOMBINASI
    def service_filter_riwayat(self, id_laptop=None, id_user=None, tanggal=None, jenis=None):
        conn = get_connection()
        try:
            repo = RiwayatAktivitasRepository(conn)
            res = repo.ambil_cari_riwayat_filter_riwayat(id_laptop, id_user, tanggal, jenis)
            return res
        finally:
            conn.close()

    # DELETE
    def service_hapus_riwayat(self, id_aktivitas):
        conn = get_connection()
        try:
            repo = RiwayatAktivitasRepository(conn)
            res = repo.hapus_riwayat_aktivitas(id_aktivitas)
            conn.commit()
            return res
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()