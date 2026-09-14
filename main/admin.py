
# Register your models here.
from django.contrib import admin
from main.models import Experience, Skill


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "started_at", "ended_at")
    list_filter = ("category",)
    search_fields = ("title", "description")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "year_started", "year_ended")
    list_filter = ("category", "proficiency")
    search_fields = ("name",)