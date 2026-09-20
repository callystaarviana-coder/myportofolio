from django.db import migrations


def seed_myportofolio_project(apps, schema_editor):
    Project = apps.get_model("main", "Project")

    Project.objects.get_or_create(
        title="MyPortofolio",
        defaults={
            "description": (
                "Website portofolio pribadi berbasis Django yang menampilkan "
                "profil, pengalaman, skills, serta daftar proyek. Website ini "
                "dibuat dan dikembangkan sebagai bagian dari mata kuliah "
                "Pemrograman Berbasis Platform."
            ),
            "tech_stack": "Python, Django, HTML, CSS, SQLite",
            "project_url": (
                "https://github.com/callystaarviana-coder/myportofolio"
            ),
            "project_image_url": (
                "https://callysta-arviana-myportofolio.pws.cs.ui.ac.id/"
                "static/img/myportofolio.png"
            ),
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_seed_portfolio_data"),
    ]

    operations = [
        migrations.RunPython(
            seed_myportofolio_project,
            migrations.RunPython.noop,
        ),
    ]