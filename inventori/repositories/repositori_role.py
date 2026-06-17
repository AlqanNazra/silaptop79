# repositories/role_repository.py
import psycopg2
from typing import List, Dict
from .interfaces.interface_role import IRoleRepository
from ..dto.dto_role import RoleDTO
from psycopg2.extras import RealDictCursor

class RoleRepository(IRoleRepository):
    def __init__(self, conn):
        self.conn = conn

    def tambah(self, data: RoleDTO) -> str:
        query = """
            SELECT tambah_role(
                %s,
                %s,
                %s,
                %s
            );
        """
        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (
                    data.nama_role,
                    data.min_ram,
                    data.min_storage,
                    data.min_processor_score
                )
            )
            result = cur.fetchone()[0]
        return result

    def update(self, data: RoleDTO) -> bool:

        query = """
            SELECT update_role(
                %s,
                %s,
                %s,
                %s,
                %s
            );
        """

        with self.conn.cursor() as cur:

            cur.execute(
                query,
                (
                    data.id_role,
                    data.nama_role,
                    data.min_ram,
                    data.min_storage,
                    data.min_processor_score
                )
            )

            result = cur.fetchone()[0]

        return result

    # def hapus(self, id_role: str) -> bool:
    #     query = "SELECT hapus_role(%s);"
    #     with self.conn.cursor() as cur:
    #         cur.execute(query, (id_role,))
    #         result = cur.fetchone()[0]
    #     return result

    def hapus(self,id_role):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM dss_bobotkriteria
                WHERE id_role_teknologi IN (
                    SELECT
                        id_role_teknologi
                    FROM role_teknologi
                    WHERE id_role = %s
                )
                """,
                (id_role,)
            )
            cur.execute(
                """
                DELETE FROM role_teknologi
                WHERE id_role = %s
                """,
                (id_role,)
            )
            cur.execute(
                """
                DELETE FROM inventori_role
                WHERE id_role = %s
                """,
                (id_role,)
            )
        return True

    def get_kriteria(self, id_role: str) -> List[Dict]:
        query = "SELECT * FROM get_kriteria_role(%s);"
        with self.conn.cursor() as cur:
            cur.execute(query, (id_role,))
            rows = cur.fetchall()
            return [{"id_kriteria": r[0], "nama_kriteria": r[1], "nilai_bobot": r[2]} for r in rows]

    def get_teknologi(
        self,
        id_role
    ):
        query = """
            SELECT
                id_role_teknologi,
                id_teknologi,
                is_default
            FROM role_teknologi
            WHERE id_role = %s
        """

        with self.conn.cursor(
            cursor_factory=RealDictCursor
        ) as cur:

            cur.execute(
                query,
                (id_role,)
            )

            return cur.fetchall()
    def get_by_id(self, id_role: str):
        query = """
            SELECT *
            FROM get_role_by_id(%s);
        """
        with self.conn.cursor() as cur:
            cur.execute(query, (id_role,))
            row = cur.fetchone()
            return row
    def get_all(self):
        query = """
            SELECT *
            FROM get_all_role();
        """
        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            return rows