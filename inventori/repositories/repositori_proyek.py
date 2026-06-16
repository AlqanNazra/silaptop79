import logging

from .interfaces.interface_repositori_proyek import IProyekRepository

logger = logging.getLogger(__name__)


class ProyekRepository(IProyekRepository):

    def __init__(self, conn):
        self.conn = conn

    # ===================================
    # TAMBAH
    # ===================================
    def tambah(self, data):
        query = """SELECT tambah_proyek(%s,%s,%s,%s);"""
        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (
                    data.nama_proyek,
                    data.user_perusahaan,
                    data.mulai_proyek,
                    data.akhir_proyek
                )
            )
            return cur.fetchone()[0]

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
                data.user_perusahaan,
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
            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None

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
            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                else:
                    return result[0]
            return None

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
            if not row:
                return {"total_role": 0, "total_teknologi": 0, "rata_bobot": 0}
            if isinstance(row, dict):
                return {
                    "total_role": row.get("total_role") or list(row.values())[0],
                    "total_teknologi": row.get("total_teknologi") or list(row.values())[1],
                    "rata_bobot": row.get("rata_bobot") or list(row.values())[2]
                }
            return {
                "total_role": row[0],
                "total_teknologi": row[1],
                "rata_bobot": row[2]
            }