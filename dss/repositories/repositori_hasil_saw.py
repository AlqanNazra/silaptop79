import psycopg2
from psycopg2.extras import RealDictCursor
from dss.dto.dto_hasil_saw import HasilSAWDTO
from interface.interface_hasil_saw import IHasilSawRepositoryImpl 


class KriteriaRepository(IHasilSawRepositoryImpl):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def buat_hasil_saw(self, data: HasilSAWDTO):
        query = """
        SELECT tambah_hasil_saw(%s, %s);
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.id_dss,
            ))
            self.conn.commit()

            return "Berhasil tambah kriteria"