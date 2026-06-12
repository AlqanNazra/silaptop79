import logging

from interfaces.interface_teknologi import ITeknologiRepository

logger = logging.getLogger(__name__)


class TeknologiRepository(ITeknologiRepository):

    def __init__(self, conn):
        self.conn = conn

    # ====================================
    # TAMBAH
    # ====================================
    def tambah_teknologi(self, data):

        query = """
        SELECT tambah_teknologi(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (
                data.nama_teknologi,
            ))

            logger.info(
                f"Berhasil tambah teknologi {data.nama_teknologi}"
            )

            return True

    # ====================================
    # UPDATE
    # ====================================
    def update_teknologi(self, data):

        query = """
        SELECT update_teknologi(%s,%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (
                data.id_teknologi,
                data.nama_teknologi
            ))

            logger.info(
                f"Berhasil update teknologi {data.id_teknologi}"
            )

            return True

    # ====================================
    # HAPUS
    # ====================================
    def hapus_teknologi(self, id_teknologi):

        query = """
        SELECT hapus_teknologi(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (id_teknologi,))

            logger.info(
                f"Berhasil hapus teknologi {id_teknologi}"
            )

            return True

    # ====================================
    # GET ALL
    # ====================================
    def get_all_teknologi(self):

        query = """
        SELECT
            id_teknologi,
            nama_teknologi,
            created_at,
            updated_at
        FROM inventori_teknologi
        ORDER BY nama_teknologi;
        """

        with self.conn.cursor() as cur:

            cur.execute(query)

            columns = [col[0] for col in cur.description]

            result = []

            for row in cur.fetchall():
                result.append(dict(zip(columns, row)))

            return result

    # ====================================
    # GET COMPATIBILITY
    # ====================================
    def get_compatibility(self, nama_teknologi):

        query = """
        SELECT *
        FROM get_compatibility_teknologi(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (nama_teknologi,))

            row = cur.fetchone()

            if not row:
                return None

            return {
                "minimal_ram": row[0],
                "minimal_core": row[1],
                "gpu_required": row[2]
            }