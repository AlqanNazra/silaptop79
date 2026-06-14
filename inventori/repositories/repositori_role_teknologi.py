import psycopg2
from psycopg2.extras import RealDictCursor
from inventori.dto.dto_role_teknologi import RoleTeknologiDTO 

from inventori.repositories.interfaces.interface_role_teknologi import (
    IRoleTeknologiRepository
)


class RoleTeknologiRepository(
    IRoleTeknologiRepository
):

    def __init__(self, conn):
        self.conn = conn

    def get_all(self):

        query = """
        SELECT *
        FROM get_all_role_teknologi();
        """

        with self.conn.cursor() as cur:

            cur.execute(query)

            rows = cur.fetchall()

            return rows

    def get_by_id(
        self,
        id_role_teknologi
    ):

        query = """
        SELECT *
        FROM get_role_teknologi_by_id(%s);
        """

        with self.conn.cursor() as cur:

            cur.execute(
                query,
                (
                    id_role_teknologi,
                )
            )

            return cur.fetchone()

    def tambah(self, data):

        query = """
        SELECT tambah_role_teknologi(
            %s,
            %s
        );
        """

        with self.conn.cursor() as cur:

            cur.execute(
                query,
                (
                    data.id_role,
                    data.id_teknologi
                )
            )

            return cur.fetchone()[0]

    def hapus(
        self,
        id_role_teknologi
    ):

        query = """
        DELETE FROM role_teknologi
        WHERE id_role_teknologi = %s;
        """

        with self.conn.cursor() as cur:

            cur.execute(
                query,
                (
                    id_role_teknologi,
                )
            )

            return True