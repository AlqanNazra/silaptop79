import logging

from django.db import transaction

class ProjectRoleValidation:

    @staticmethod
    def validate_input(data):

        if not data.id_proyek:
            raise ValueError(
                "ID proyek wajib diisi"
            )

        if not data.id_role:
            raise ValueError(
                "ID role wajib diisi"
            )

        return True

logger = logging.getLogger(__name__)


class ProjectRoleService:

    def __init__(
        self,
        projectrole_repo,
        conn
    ):
        self.projectrole_repo = projectrole_repo
        self.conn = conn

    def tambah_projectrole(self, data):

        ProjectRoleValidation.validate_input(
            data
        )

        try:

            with transaction.atomic():

                is_valid = (
                    self.projectrole_repo
                    .validate_relation(
                        data.id_proyek,
                        data.id_role
                    )
                )
                if not is_valid:
                    raise Exception(
                        "Relasi project-role tidak valid"
                    )

                self.projectrole_repo.tambah(
                    data
                )
                self.conn.commit()

                logger.info(
                    f"Tambah projectrole sukses "
                    f"{data.id_proyek}"
                )

                return {
                    "success": True,
                    "message":
                    "Berhasil tambah projectrole"
                }

        except Exception as e:

            self.conn.rollback()

            logger.error(str(e))

            raise Exception(str(e))

    def hapus_projectrole(
        self,
        id_projectrole,
        id_proyek=None
    ):

        try:

            with transaction.atomic():

                self.projectrole_repo.hapus(
                    id_projectrole
                )

                # update DSS
                if id_proyek:
                    self.recalculate_dss(
                        id_proyek
                    )

                self.conn.commit()

                return {
                    "success": True,
                    "message":
                    "Berhasil hapus projectrole"
                }

        except Exception as e:

            self.conn.rollback()

            logger.error(str(e))

            raise Exception(str(e))

    def getByProject(self, id_proyek):

        return (
            self.projectrole_repo
            .get_by_project(id_proyek)
        )

    def getByRole(self, id_role):

        return (
            self.projectrole_repo
            .get_by_role(id_role)
        )

    def validateRelation(
        self,
        id_proyek,
        id_role
    ):

        return (
            self.projectrole_repo
            .validate_relation(
                id_proyek,
                id_role
            )
        )