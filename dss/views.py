from django.shortcuts import render

from .services.service_swara import ServiceBobotKriteria
from .services.service_bobotkriteria import ServiceBobotKriteria
from db import get_connection


import json

def testing_swara(request):
    conn =  get_connection()
    result = None
    error = None
    data = None
    selected_roles = []

    service = ServiceBobotKriteria(conn)

    if request.method == "POST":
        action = request.POST.get("action")

        try:
            if action == "input_bobot":
                role = request.POST.get("role")

                nama_list = request.POST.getlist("nama[]")
                tipe_list = request.POST.getlist("tipe[]")
                bobot_list = request.POST.getlist("bobot[]")

                list_kriteria = []

                for i in range(len(nama_list)):
                    if nama_list[i] and bobot_list[i]:
                        list_kriteria.append({
                            "nama": nama_list[i],
                            "tipe": tipe_list[i],
                            "bobot": float(bobot_list[i])
                        })

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

        except Exception as e:
            error = str(e)

    return render(request, "testing_swara.html", {
        "result": result,
        "error": error,
        "data": data,
        "roles_list": ["backend","frontend","mobile"],
        "selected_roles": selected_roles
    })