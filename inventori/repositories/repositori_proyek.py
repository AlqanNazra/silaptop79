import logging

from interfaces.interface_repositori_proyek import IProyekRepository

logger = logging.getLogger(__name__)


class ProyekRepository(IProyekRepository):

    def __init__(self, conn):
        self.conn = conn

    # ===================================
    # TAMBAH
    # ===================================
    def tambah(self, data):

        query = """
        SELECT tambah_proyek(%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (
                data.nama_proyek,
                data.client_perusahaan,
                data.mulai_proyek,
                data.akhir_proyek
            ))

            logger.info(
                f"Tambah proyek sukses "
                f"{data.nama_proyek}"
            )

            return True

    # ===================================
    # UPDATE
    # ===================================
    def update(self, data):

        query = """
        SELECT update_proyek(%s,%s,%s,%s,%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (
                data.id_proyek,
                data.nama_proyek,
                data.client_perusahaan,
                data.mulai_proyek,
                data.akhir_proyek
            ))

            return True

    # ===================================
    # HAPUS
    # ===================================
    def hapus(self, id_proyek):

        query = """
        SELECT hapus_proyek(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (id_proyek,))

            return True

    # ===================================
    # GET BOBOT
    # ===================================
    def get_bobot(self, id_proyek):

        query = """
        SELECT get_bobot_proyek(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (id_proyek,))

            result = cur.fetchone()

            return result[0]

    # ===================================
    # VALIDATE
    # ===================================
    def validate(self, id_proyek):

        query = """
        SELECT validate_proyek(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (id_proyek,))

            result = cur.fetchone()

            return result[0]

    # ===================================
    # GET ROLES
    # ===================================
    def get_roles(self, id_proyek):

        query = """
        SELECT * FROM get_roles_proyek(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (id_proyek,))

            columns = [col[0] for col in cur.description]

            result = []

            for row in cur.fetchall():
                result.append(dict(zip(columns, row)))

            return result

    # ===================================
    # GET TEKNOLOGI
    # ===================================
    def get_teknologi(self, id_proyek):

        query = """
        SELECT * FROM get_teknologi_proyek(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (id_proyek,))

            columns = [col[0] for col in cur.description]

            result = []

            for row in cur.fetchall():
                result.append(dict(zip(columns, row)))

            return result

    # ===================================
    # GET SUMMARY
    # ===================================
    def get_summary(self, id_proyek):

        query = """
        SELECT * FROM get_summary_proyek(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (id_proyek,))

            row = cur.fetchone()

            return {
                "total_role": row[0],
                "total_teknologi": row[1],
                "rata_bobot": row[2]
            }