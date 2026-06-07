import psycopg2
from psycopg2.extras import RealDictCursor
from dss.repositories.dto.dto_laptop_alternatif import LaptopAlternatifDTO

class LaptopAlternatifRepository:
    def __init__(self, conn):
        self.conn = conn

    def tambah_laptop_alternatif(self, data: LaptopAlternatifDTO):
        query = """
        SELECT tambah_laptop_alternatif(%s, %s, %s);
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (
                data.model_alternatif,
                data.brand_alternatif,
                data.id_dss
            ))
            self.conn.commit()
            return "Berhasil tambah laptop alternatif"
