import logging

from interfaces.interface_repositori_proyek import IProyekRepository

logger = logging.getLogger(__name__)


class ProjectRoleRepository(
    IProjectRoleRepository
):

    def __init__(self, conn):
        self.conn = conn

    def tambah(self, data):

        query = """
        SELECT tambah_projectrole(%s,%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (
                data.id_proyek,
                data.id_role
            ))

            logger.info(
                f"Tambah projectrole "
                f"{data.id_proyek} - {data.id_role}"
            )

            return True

    def hapus(self, id_projectrole):

        query = """
        SELECT hapus_projectrole(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (
                id_projectrole,
            ))

            logger.info(
                f"Hapus projectrole "
                f"{id_projectrole}"
            )

            return True

    def get_by_project(self, id_proyek):

        query = """
        SELECT *
        FROM get_projectrole_by_project(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (id_proyek,))

            columns = [col[0] for col in cur.description]

            result = []

            for row in cur.fetchall():
                result.append(dict(zip(columns, row)))

            return result

    def get_by_role(self, id_role):

        query = """
        SELECT *
        FROM get_projectrole_by_role(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (id_role,))

            columns = [col[0] for col in cur.description]

            result = []

            for row in cur.fetchall():
                result.append(dict(zip(columns, row)))

            return result

    def validate_relation(
        self,
        id_proyek,
        id_role
    ):

        query = """
        SELECT validate_projectrole_relation(
            %s,
            %s
        );
        """

        with self.conn.cursor() as cur:

            cur.execute(query, (
                id_proyek,
                id_role
            ))

            result = cur.fetchone()

            return result[0]