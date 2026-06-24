import logging

from django.db import transaction

logger = logging.getLogger(__name__)


class RoleTeknologiService:

    def __init__(
        self,
        role_teknologi_repo,
        conn
    ):
        self.role_teknologi_repo = (
            role_teknologi_repo
        )
        self.conn = conn

    def get_all(self):
        return (
            self.role_teknologi_repo
            .get_all()
        )

    def get_by_id(
        self,
        id_role_teknologi
    ):
        return (
            self.role_teknologi_repo
            .get_by_id(
                id_role_teknologi
            )
        )

    def tambah(self, data):
        try:
            with transaction.atomic():
                result = (
                    self.role_teknologi_repo
                    .tambah(data)
                )
                self.conn.commit()
                return result
        except Exception as e:
            self.conn.rollback()
            logger.error(str(e))
            raise Exception(str(e))

    def hapus(
        self,
        id_role_teknologi
    ):
        try:
            with transaction.atomic():
                result = (
                    self.role_teknologi_repo
                    .hapus(
                        id_role_teknologi
                    )
                )
                self.conn.commit()
                return result
        except Exception as e:
            self.conn.rollback()
            logger.error(str(e))
            raise Exception(str(e))
        
    def hapus_by_role(self,id_role):
        query = """
        DELETE
        FROM role_teknologi
        WHERE id_role = %s
        """
        with self.conn.cursor() as cur:
            cur.execute(
                query,
                (id_role,)
            )
            return True