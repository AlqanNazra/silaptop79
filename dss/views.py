from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .services.service_swara import ServiceSwara
from .services.service_bobotkriteria import ServiceBobotKriteria
from core.db import get_connection

import json

# @login_required
def testing_swara(request):
    conn =  get_connection()
    result = None
    error = None
    data = None
    selected_roles = []
    roles_list = []

    service = ServiceBobotKriteria(conn)
    roles_result = service.get_unique_roles()
    roles_list = roles_result.get("data", [])

    if request.method == "POST":
        action = request.POST.get("action")

        try:
            if action == "input_bobot":
                role = request.POST.get("role")

                nama_list = request.POST.getlist("nama[]")
                tipe_list = request.POST.getlist("tipe[]")
                bobot_list = request.POST.getlist("bobot[]")

                list_kriteria = []

                golongan = request.POST.get("role") 

                for i in range(len(nama_list)):
                    list_kriteria.append({
                        "nama": nama_list[i].strip(),
                        "tipe": tipe_list[i],
                        "bobot": float(bobot_list[i]),
                        "golongan": golongan   # sama semua
                    })
                print("nama:", nama_list)
                print("tipe:", tipe_list)
                print("bobot:", bobot_list)
                print("golongan:", golongan)

                result = service.input_bobot_batch(role, list_kriteria)

            elif action == "ambil_kriteria":
                result = service.ambil_kriteria()
                data = result.get("data")

            elif action == "update_kriteria":
                result = service.update_kriteria(
                    request.POST.get("id_kriteria"),
                    request.POST.get("nama"),
                    request.POST.get("tipe")
                )

            elif action == "ambil_bobot":
                selected_roles = request.POST.getlist("roles")
                result = service.ambil_bobot_by_roles(selected_roles)
                data = result.get("data")
                
            elif action == "ambil_bobot_by_kriteria":
                result = service.ambil_bobot_by_kriteria(
                    request.POST.get("id_bobot"),
                    request.POST.get("id_kriteria")
                )
                data = result.get("data")

            elif action == "update_bobot":
                result = service.update_bobot(
                    request.POST.get("id_bobot"),
                    float(request.POST.get("nilai_bobot"))
                )

            elif action == "hapus_bobot":
                result = service.hapus_bobot(
                    request.POST.get("id_bobot")
                )
            elif action == "load_kriteria_swara":
                selected_roles = request.POST.getlist("roles")
                result = service.ambil_bobot_by_roles(selected_roles)
                data = result.get("data")

            elif action == "proses_swara":
                selected_roles = request.POST.getlist("roles")

                swara_service = ServiceSwara(conn)

                result = swara_service.proses_swara(selected_roles, None)
                data = result.get("data")        

        except Exception as e:
            error = str(e)

    return render(request, "testing_swara.html", {
        "result": result,
        "error": error,
        "data": data,
        "roles_list": roles_list,
        "selected_roles": selected_roles
    })