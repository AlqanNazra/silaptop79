import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "silaptop79.settings")
django.setup()

from inventori.models import Proyek, Role, Teknologi, RoleTeknologi, ProjectRole, User
from dss.models import Kriteria, BobotKriteria
from django.utils import timezone

def seed():
    print("Seed helper running...")
    
    # 1. Ensure Kriteria exists
    kriterias = {}
    kriteria_data = [
        ("processor", "benefit"),
        ("ram", "benefit"),
        ("storage", "benefit"),
        ("berat", "cost"),
        ("layar", "benefit"),
        ("baterai", "benefit")
    ]
    for idx, (name, tipe) in enumerate(kriteria_data, 1):
        k_id = f"KRIT_000{idx}"
        k, created = Kriteria.objects.get_or_create(
            id_kriteria=k_id,
            defaults={
                "nama_kriteria": name,
                "tipe_kriteria": tipe,
                "golongan_kriteria": "hardware" if idx <= 3 else "fisik"
            }
        )
        kriterias[name] = k
        if created:
            print(f"Created Kriteria {name}")
            
    # 2. Roles
    roles = {}
    roles_data = [
        ("ROLE_0001", "Backend Developer", 16, 512, 75),
        ("ROLE_0002", "Frontend Developer", 8, 256, 60),
    ]
    for r_id, r_name, ram, storage, proc_score in roles_data:
        r, created = Role.objects.get_or_create(
            id_role=r_id,
            defaults={
                "nama_role": r_name,
                "min_ram": ram,
                "min_storage": storage,
                "min_processor_score": proc_score
            }
        )
        roles[r_name] = r
        if created:
            print(f"Created Role {r_name}")
            
    # 3. Teknologi
    teks = {}
    teks_data = [
        ("TEK_0001", "Spring Boot", "Backend"),
        ("TEK_0002", "ReactJS", "Frontend")
    ]
    for t_id, t_name, kat in teks_data:
        t, created = Teknologi.objects.get_or_create(
            id_teknologi=t_id,
            defaults={
                "nama_teknologi": t_name,
                "kategori": kat
            }
        )
        teks[t_name] = t
        if created:
            print(f"Created Teknologi {t_name}")
            
    # 4. RoleTeknologi
    rt1, created1 = RoleTeknologi.objects.get_or_create(
        id_role_teknologi="ROLETEK_0001",
        defaults={
            "role": roles["Backend Developer"],
            "teknologi": teks["Spring Boot"]
        }
    )
    rt2, created2 = RoleTeknologi.objects.get_or_create(
        id_role_teknologi="ROLETEK_0002",
        defaults={
            "role": roles["Frontend Developer"],
            "teknologi": teks["ReactJS"]
        }
    )
    if created1 or created2:
        print("Created RoleTeknologi links")
        
    # 5. BobotKriteria
    for idx, (k_name, k_obj) in enumerate(kriterias.items(), 1):
        BobotKriteria.objects.get_or_create(
            id_bobot=f"B_BE_{k_name}",
            defaults={
                "id_kriteria": k_obj,
                "role": "Backend Developer",
                "nilai_bobot": 0.2 if idx <= 2 else 0.15
            }
        )
        BobotKriteria.objects.get_or_create(
            id_bobot=f"B_FE_{k_name}",
            defaults={
                "id_kriteria": k_obj,
                "role": "Frontend Developer",
                "nilai_bobot": 0.2 if idx <= 2 else 0.15
            }
        )
        
    # 6. Proyek
    p, created = Proyek.objects.get_or_create(
        id_proyek="PRYK_0001",
        defaults={
            "nama_proyek": "Sistem Informasi Akademik"
        }
    )
    if created:
        print("Created Proyek Sistem Informasi Akademik")
        
    # 7. ProjectRole Link
    ProjectRole.objects.get_or_create(
        id_project_role="PRJROLE_0001",
        defaults={
            "proyek": p,
            "role": roles["Backend Developer"],
            "persentase_role": 0.5
        }
    )
    ProjectRole.objects.get_or_create(
        id_project_role="PRJROLE_0002",
        defaults={
            "proyek": p,
            "role": roles["Frontend Developer"],
            "persentase_role": 0.5
        }
    )
    print("Seed helper finished successfully!")

if __name__ == "__main__":
    seed()
