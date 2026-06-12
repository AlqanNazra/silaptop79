from django.db import connection
import uuid

class DSSRepository:
    
    @staticmethod
    def get_bobot_role_teknologi(id_role_teknologi: uuid.UUID) -> list:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM get_bobot_role_teknologi(%s)", [str(id_role_teknologi)])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def update_nilai_swara(id_bobot: uuid.UUID, nilai_swara: float) -> None:
        with connection.cursor() as cursor:
            cursor.execute("SELECT update_nilai_swara(%s, %s)", [str(id_bobot), nilai_swara])

    @staticmethod
    def get_project_roles(id_proyek: uuid.UUID) -> list:
        with connection.cursor() as cursor:
            query = """
                SELECT pr.id_role, r.nama_role, pr.persentase_role
                FROM project_role pr
                JOIN role r ON pr.id_role = r.id_role
                WHERE pr.id_proyek = %s
            """
            cursor.execute(query, [str(id_proyek)])
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @staticmethod
    def validasi_project_roles(id_proyek: uuid.UUID) -> bool:
        with connection.cursor() as cursor:
            cursor.execute("SELECT validasi_total_bobot_project(%s)", [str(id_proyek)])
            return cursor.fetchone()[0]