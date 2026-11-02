from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Education
from main.serializers import EducationSerializer


class EducationAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser(username="owner", password="test-password")
        cls.visitor = User.objects.create_user(username="visitor", password="test-password")
        cls.editor = User.objects.create_user(username="editor", password="test-password")
        cls.editor.groups.add(Group.objects.create(name="Editor"))
        cls.education = Education.objects.create(
            institution="Universitas Indonesia", degree="S1 Sistem Informasi",
            description="Pendidikan saat ini", year_started=2025, is_current=True,
        )

    def setUp(self):
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.pk])
        self.star_url = reverse("api:education-star", args=[self.education.pk])
        self.payload = {
            "institution": "SMA Kolese Gonzaga", "degree": "SMA",
            "description": "Pendidikan menengah", "year_started": 2022,
            "year_ended": 2025, "is_current": False,
        }

    def test_public_list_detail_and_search(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], self.education.pk)
        self.assertNotIn("fields", response.data[0])
        self.assertFalse(response.data[0]["is_starred"])
        self.assertEqual(self.client.get(self.detail_url).status_code, 200)
        response = self.client.get(self.list_url, {"institution": "INDONESIA"})
        self.assertEqual(len(response.data), 1)
        self.assertEqual(self.client.get(self.list_url, {"institution": "missing"}).data, [])

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"degree": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 Sistem Informasi")

    def test_editor_can_patch_and_put_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"degree": "S1 SI"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.education.refresh_from_db()
        self.assertEqual(self.education.degree, "S1 SI")
        self.assertEqual(self.education.institution, "Universitas Indonesia")
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Education.objects.count(), 1)

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["year_ended"], 2025)
        self.assertEqual(self.client.put(self.detail_url, {"degree": "Incomplete"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertEqual(self.client.get(self.detail_url).status_code, 404)

    def test_validation_rejects_html_only_text_and_invalid_years(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"institution": "   "}, "institution"),
            ({"institution": "<img src=x>"}, "institution"),
            ({"degree": "<b></b>"}, "degree"),
            ({"description": "<br>"}, "description"),
            ({"year_started": -1}, "year_started"),
            ({"year_ended": 2020}, "year_ended"),
            ({"year_ended": None}, "year_ended"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, 400, changes)
            self.assertIn(field, response.data)
        self.assertEqual(Education.objects.count(), 1)

    def test_partial_validation_uses_existing_years(self):
        self.client.force_authenticate(user=self.editor)
        response = self.client.patch(self.detail_url, {"is_current": False}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("year_ended", response.data)
        response = self.client.patch(self.detail_url, {"is_current": False, "year_ended": 2026}, format="json")
        self.assertEqual(response.status_code, 200)
        response = self.client.patch(self.detail_url, {"year_started": 2027}, format="json")
        self.assertEqual(response.status_code, 400)
        self.education.refresh_from_db()
        self.assertEqual(self.education.year_started, 2025)

    def test_current_education_clears_end_year_and_cleans_text(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "institution": "<b>Sekolah</b>", "is_current": True,
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["institution"], "Sekolah")
        self.assertIsNone(response.data["year_ended"])

    def test_star_uses_authenticated_user_and_read_only_fields(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url, {"user": self.owner.pk}, format="json")
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(self.education.starred_by.filter(pk=self.visitor.pk).exists())
        self.assertFalse(self.education.starred_by.filter(pk=self.owner.pk).exists())
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "id": 99999, "star_count": 99,
            "is_starred": True, "starred_by": [self.visitor.pk],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], 99999)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertNotIn("starred_by", response.data)

    def test_wrong_methods_and_safe_methods_never_change_data(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.assertEqual(self.client.head(self.detail_url).status_code, 200)
        self.assertEqual(self.client.options(self.detail_url).status_code, 200)
        self.assertEqual(Education.objects.count(), 1)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_session_csrf_on_create_patch_and_delete(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.owner)
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(client.patch(self.detail_url, {"degree": "Updated"}, format="json").status_code, 403)
        self.assertEqual(client.delete(self.detail_url).status_code, 403)
        response = client.get(reverse("main:show_education"))
        self.assertEqual(response.status_code, 200)
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token).status_code, 201)
        self.assertEqual(client.patch(self.detail_url, {"degree": "Updated"}, format="json", HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(client.delete(self.detail_url, HTTP_X_CSRFTOKEN=token).status_code, 204)

    def test_regular_user_receives_csrf_cookie_and_can_star(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.visitor)
        page = client.get(reverse("main:show_education"))
        self.assertNotContains(page, 'id="education-form"')
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.star_url, HTTP_X_CSRFTOKEN=token).status_code, 200)

    def test_editor_legacy_edit_page_still_works(self):
        self.client.force_login(self.editor)
        url = reverse("main:update_education", args=[self.education.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        response = self.client.post(url, self.payload)
        self.assertRedirects(response, reverse("main:show_education"))
        self.education.refresh_from_db()
        self.assertEqual(self.education.institution, "SMA Kolese Gonzaga")

    def test_serializer_without_request(self):
        self.assertFalse(EducationSerializer(self.education).data["is_starred"])

    def test_malformed_json_and_missing_object(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, '{"broken":', content_type="application/json")
        self.assertEqual(response.status_code, 400)
        url = reverse("api:education-detail", args=[99999])
        self.assertEqual(self.client.get(url).status_code, 404)
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.patch(url, {"degree": "No"}, format="json").status_code, 403)
