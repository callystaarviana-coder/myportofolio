import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required  # Tambahkan baris ini
from django.core.exceptions import PermissionDenied        # Tambahkan baris ini

from main.forms import EducationForm, ProjectForm
from main.models import Education, Experience, Project, Skill

def show_main(request):
    last_login = request.COOKIES.get(
        "last_login",
        "Belum ada sesi login / Cookie tidak ditemukan",
    )

    context = {
        "name": "Callysta Arviana",
        "npm": "2506619045",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Mahasiswa Sistem Informasi Universitas Indonesia yang mendalami "
            "bidang Project Management dan Web Development."
        ),
        "last_login": last_login,
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

@login_required(login_url="/login/")
def create_project(request):

    if not request.user.is_superuser:
        raise PermissionDenied

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
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    data = []

    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )
        starred_by_names = ", ".join(
            user.username for user in starred_users
        )

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            },
        })

    return JsonResponse(data, safe=False)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Callysta Arviana",
        "title_query": title_query,
        "form": ProjectForm(),
    }

    return render(request, "project.html", context)

@login_required(login_url="/login/")
def delete_project(request, project_id):

    if not request.user.is_superuser:
        raise PermissionDenied
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

@login_required(login_url="/login/")
def create_education(request):
    if not request.user.is_superuser:
        raise PermissionDenied

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


@login_required(login_url="/login/")
def update_education(request, education_id):
    is_editor = request.user.groups.filter(name="Editor").exists()

    if not (request.user.is_superuser or is_editor):
        raise PermissionDenied

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


@login_required(login_url="/login/")
@require_POST
def delete_education(request, education_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    education = get_object_or_404(Education, pk=education_id)
    education.delete()

    messages.success(request, "Data pendidikan berhasil dihapus.")
    return redirect("main:show_education")


def get_education_json(request):
    education_list = Education.objects.order_by("-year_started", "-pk")

    data = serializers.serialize(
        "json",
        education_list,
        use_natural_foreign_keys=True,
    )

    return HttpResponse(data, content_type="application/json")


def show_education(request):
    json_response = get_education_json(request)

    education_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    education_list = [item.object for item in education_data]

    is_editor = (
        request.user.is_authenticated
        and request.user.groups.filter(name="Editor").exists()
    )

    context = {
        "name": "Callysta Arviana",
        "education_list": education_list,
        "is_editor": is_editor,
    }
    return render(request, "education.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Callysta Arviana",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        response = redirect("main:show_main")
        response.set_cookie(
            "last_login",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        return response

    context = {
        "name": "Callysta Arviana",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")

@login_required(login_url="/login/")
@require_POST
def toggle_education_star(request, education_id):
    education = get_object_or_404(Education, pk=education_id)

    if education.starred_by.filter(pk=request.user.pk).exists():
        education.starred_by.remove(request.user)
    else:
        education.starred_by.add(request.user)

    return redirect("main:show_education")

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": "Hanya pemilik portofolio yang dapat menambahkan proyek."
            },
            status=403,
        )

    form = ProjectForm(request.POST)

    if form.is_valid():
        project = form.save()

        return JsonResponse(
            {
                "message": "Proyek berhasil ditambahkan.",
                "pk": str(project.id),
            },
            status=201,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )