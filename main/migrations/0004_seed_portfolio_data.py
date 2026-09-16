from django.db import migrations


def seed_portfolio_data(apps, schema_editor):
    Skill = apps.get_model("main", "Skill")
    Experience = apps.get_model("main", "Experience")

    skills = [
        {
            "name": "Python",
            "category": "technical",
            "proficiency": "intermediate",
            "year_started": 2025,
            "year_ended": None,
        },
        {
            "name": "Java",
            "category": "technical",
            "proficiency": "beginner",
            "year_started": 2026,
            "year_ended": None,
        },
        {
            "name": "HTML",
            "category": "technical",
            "proficiency": "beginner",
            "year_started": 2024,
            "year_ended": None,
        },
        {
            "name": "Canva",
            "category": "technical",
            "proficiency": "advanced",
            "year_started": 2019,
            "year_ended": None,
        },
        {
            "name": "CapCut",
            "category": "technical",
            "proficiency": "advanced",
            "year_started": 2021,
            "year_ended": None,
        },
        {
            "name": "Problem Solving",
            "category": "soft_skill",
            "proficiency": "intermediate",
            "year_started": 2023,
            "year_ended": None,
        },
        {
            "name": "Communication",
            "category": "soft_skill",
            "proficiency": "advanced",
            "year_started": 2023,
            "year_ended": None,
        },
        {
            "name": "Leadership",
            "category": "soft_skill",
            "proficiency": "intermediate",
            "year_started": 2024,
            "year_ended": None,
        },
        {
            "name": "Japanese",
            "category": "soft_skill",
            "proficiency": "beginner",
            "year_started": 2024,
            "year_ended": None,
        },
        {
            "name": "Chinese",
            "category": "soft_skill",
            "proficiency": "beginner",
            "year_started": 2024,
            "year_ended": None,
        },
        {
            "name": "English",
            "category": "soft_skill",
            "proficiency": "advanced",
            "year_started": 2020,
            "year_ended": None,
        },
        {
            "name": "Indonesian",
            "category": "soft_skill",
            "proficiency": "advanced",
            "year_started": 2007,
            "year_ended": None,
        },
    ]

    experiences = [
        {
            "title": "Staff BEM Fasilkom UI 2026",
            "description": (
                "Berada pada bidang keilmuan yang membantu "
                "kontingen CS UI dalam berlomba."
            ),
            "category": "part-time",
        },
        {
            "title": "OH Fasilkom UI 2026",
            "description": (
                "Staff Public Relations, bertugas menjadi MC "
                "dan penghubung dalam acara."
            ),
            "category": "part-time",
        },
        {
            "title": "OIM UI 2025",
            "description": (
                "Staff Debat, bertugas menjadi LO "
                "dan pengawas lomba."
            ),
            "category": "part-time",
        },
    ]

    for skill in skills:
        Skill.objects.get_or_create(
            name=skill["name"],
            defaults=skill,
        )

    for experience in experiences:
        Experience.objects.get_or_create(
            title=experience["title"],
            defaults=experience,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_project"),
    ]

    operations = [
        migrations.RunPython(
            seed_portfolio_data,
            migrations.RunPython.noop,
        ),
    ]