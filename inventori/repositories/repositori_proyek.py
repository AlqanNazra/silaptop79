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
            result = cur.fetchone()

            print("FETCHONE =", result)

            if result:
                print("RESULT[0] =", result[0])
                print("TYPE =", type(result[0]))

            return result[0]

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

            cur.execute(
                query,
                (id_proyek,)
            )

            result = cur.fetchone()

            if result:
                return result[0]

            return False

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
            cur.execute(query,(id_proyek,))
            result = cur.fetchone()
            if result:
                if isinstance(result, dict):
                    return list(result.values())[0]
                return result[0]
            return False

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

    def ambil_by_id(self,id_proyek):
        query = """
        SELECT
            id_proyek,
            nama_proyek
        FROM inventori_proyek
        WHERE id_proyek = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query,(id_proyek,))
            row = cur.fetchone()
            if not row:
                return None
            return {
                "id_proyek": row[0],
                "nama_proyek": row[1]
            }
    def ambil_by_id_full_proyek(self,id_proyek):
        query = """
        SELECT
            p.id_proyek,
            p.nama_proyek,
            p.user_perusahaan,
            p.mulai_proyek,
            p.akhir_proyek
        FROM inventori_proyek p
        WHERE p.id_proyek = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(query,(id_proyek,))
            row = cur.fetchone()
            if not row:
                return None
            proyek = {
                "id_proyek": row[0],
                "nama_proyek": row[1],
                "user_perusahaan": row[2],
                "mulai_proyek": row[3],
                "akhir_proyek": row[4],
                "roles": []
            }
            cur.execute("""
                SELECT
                    pr.id_project_role,
                    r.id_role,
                    r.nama_role,
                    pr.persentase_role
                FROM inventori_project_role pr
                JOIN inventori_role r
                    ON r.id_role = pr.id_role
                WHERE pr.id_proyek = %s
                ORDER BY r.nama_role
            """, (id_proyek,))
            for role_row in cur.fetchall():
                proyek["roles"].append({
                    "id_role": role_row[1],
                    "nama_role": role_row[2],
                    "persentase_role": role_row[3]
                })
            return proyek
        
    def ambil_role_proyek(self,id_proyek):
        query = """
        SELECT
            pr.id_project_role,
            r.id_role,
            r.nama_role,
            pr.persentase_role
        FROM inventori_project_role pr
        INNER JOIN inventori_role r
            ON r.id_role = pr.id_role
        WHERE pr.id_proyek = %s
        ORDER BY r.nama_role;
        """
        with self.conn.cursor() as cur:
            cur.execute(query,(id_proyek,))
            rows = cur.fetchall()
            hasil = []
            for row in rows:
                hasil.append({
                    "id_project_role": row[0],
                    "id_role": row[1],
                    "nama_role": row[2],
                    "persentase_role": row[3]
                })
            return hasil