from django.forms import ModelForm, TextInput, Textarea, URLInput
from main.models import Project, Education

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }

class EducationForm(ModelForm):
    class Meta:
        model = Education
        fields = [
            "institution",
            "degree",
            "description",
            "year_started",
            "year_ended",
            "is_current",
        ]

        labels = {
            "institution": "Nama Sekolah / Universitas",
            "degree": "Jenjang / Program Studi",
            "description": "Deskripsi",
            "year_started": "Tahun Masuk",
            "year_ended": "Tahun Selesai",
            "is_current": "Masih menempuh pendidikan",
        }

        widgets = {
            "description": Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        year_started = cleaned_data.get("year_started")
        year_ended = cleaned_data.get("year_ended")
        is_current = cleaned_data.get("is_current")

        if is_current:
            cleaned_data["year_ended"] = None
        elif year_ended is None:
            self.add_error(
                "year_ended",
                "Isi tahun selesai atau centang masih menempuh pendidikan.",
            )
        elif year_started is not None and year_ended < year_started:
            self.add_error(
                "year_ended",
                "Tahun selesai tidak boleh sebelum tahun masuk.",
            )

        return cleaned_data