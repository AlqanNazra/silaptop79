import psycopg2
from psycopg2.extras import RealDictCursor
from .dto.dto_hasil_saw import HasilSAWDTO
from .interface.interface_hasil_saw import IHasilSawRepositoryImpl 


class HasilSawRepository(IHasilSawRepositoryImpl):

    def __init__(self, conn):
        self.conn = conn

    # =========================
    # CREATE
    # =========================
    def buat_hasil_saw(self, data: HasilSAWDTO):

        query = """
        SELECT buat_hasil_saw(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(
                query,
                (
                    data.id_dss,
                )
            )

            hasil = cur.fetchone()

            print("\n=== DEBUG HASIL SAW ===")
            print(hasil)

            self.conn.commit()

            if isinstance(hasil, tuple):
                return hasil[0]

            if isinstance(hasil, dict):
                return next(iter(hasil.values()))

            return hasil