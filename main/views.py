from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import EducationForm, ProjectForm
from main.models import Education, Experience, Project, Skill

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

def show_skills(request):
    all_skills = Skill.objects.all()
    context = {
        "name": "Callysta Arviana",
        "skill_list": all_skills, 
        "technical_skills": all_skills.filter(category="technical"),
        "soft_skills": all_skills.filter(category="soft_skill"),
        "total_skills": all_skills.count(),
    }
    return render(request, "skills.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Callysta Arviana",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Callysta Arviana",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def create_education(request):
    form = EducationForm(
        request.POST if request.method == "POST" else None
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data pendidikan berhasil ditambahkan.")
        return redirect("main:show_education")

    context = {
        "name": "Callysta Arviana",
        "form": form,
        "page_title": "Tambah Pendidikan",
    }
    return render(request, "education_form.html", context)


def update_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    form = EducationForm(
        request.POST if request.method == "POST" else None,
        instance=education,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Data pendidikan berhasil diperbarui.")
        return redirect("main:show_education")

    context = {
        "name": "Callysta Arviana",
        "form": form,
        "page_title": "Edit Pendidikan",
    }
    return render(request, "education_form.html", context)


@require_POST
def delete_education(request, education_id):
    education = get_object_or_404(Education, pk=education_id)
    education.delete()
    messages.success(request, "Data pendidikan berhasil dihapus.")
    return redirect("main:show_education")


def get_education_json(request):
    education_list = Education.objects.order_by("-year_started", "-pk")
    data = serializers.serialize("json", education_list)
    return HttpResponse(data, content_type="application/json")


def show_education(request):
    json_response = get_education_json(request)

    education_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [item.object for item in education_data]

    context = {
        "name": "Callysta Arviana",
        "education_list": education_list,
    }
    return render(request, "education.html", context)

