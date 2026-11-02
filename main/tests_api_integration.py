from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Project
from main.serializers import ProjectSerializer


class APIIntegrationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser(username="integration-owner", password="test-password")
        cls.visitor = User.objects.create_user(username="integration-visitor", password="test-password")
        cls.project = Project.objects.create(title="Integration", description="Description", tech_stack="Django")

    def test_existing_pages_and_legacy_json_endpoints_remain_accessible(self):
        for name in [
            "main:show_main", "main:show_experience", "main:show_skills",
            "main:show_projects", "main:show_education", "main:get_projects_json",
            "main:get_education_json", "contacts:contact_list",
        ]:
            self.assertEqual(self.client.get(reverse(name)).status_code, 200, name)

    def test_regular_user_projects_page_creates_csrf_cookie_for_star(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.visitor)
        page = client.get(reverse("main:show_projects"))
        self.assertContains(page, reverse("api:project-list"))
        self.assertNotContains(page, 'id="project-form"')
        token = client.cookies["csrftoken"].value
        url = reverse("api:project-star", args=[self.project.pk])
        self.assertEqual(client.post(url, HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertTrue(self.project.starred_by.filter(pk=self.visitor.pk).exists())

    def test_project_session_csrf_is_required_for_patch_and_delete(self):
        client = APIClient(enforce_csrf_checks=True)
        client.force_login(self.owner)
        url = reverse("api:project-detail", args=[self.project.pk])
        self.assertEqual(client.patch(url, {"title": "Updated"}, format="json").status_code, 403)
        self.assertEqual(client.delete(url).status_code, 403)
        client.get(reverse("main:show_projects"))
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.patch(url, {"title": "Updated"}, format="json", HTTP_X_CSRFTOKEN=token).status_code, 200)
        self.assertEqual(client.delete(url, HTTP_X_CSRFTOKEN=token).status_code, 204)

    def test_project_serializer_without_request_and_star_actor(self):
        self.assertFalse(ProjectSerializer(self.project).data["is_starred"])
        self.client.force_authenticate(user=self.visitor)
        url = reverse("api:project-star", args=[self.project.pk])
        response = self.client.post(url, {"user": self.owner.pk}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["starred_by_names"], self.visitor.username)
        self.assertFalse(self.project.starred_by.filter(pk=self.owner.pk).exists())

    def test_project_safe_methods_and_malformed_json(self):
        url = reverse("api:project-detail", args=[self.project.pk])
        self.assertEqual(self.client.head(url).status_code, 200)
        self.assertEqual(self.client.options(url).status_code, 200)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Integration")
        self.assertEqual(self.project.starred_by.count(), 0)
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(url, '{"broken":', content_type="application/json")
        self.assertEqual(response.status_code, 400)
