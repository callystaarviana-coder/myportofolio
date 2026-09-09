from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Callysta Arviana",
        "npm": "2506619045",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang mandalami  "
            "bidang Project Management dan Web Development."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Callysta Arviana",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)