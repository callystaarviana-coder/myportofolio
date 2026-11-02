from urllib.parse import urlencode

from django.test import Client, TestCase
from django.urls import reverse

from .models import Contact


class ContactTests(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="Ani", email="ani@example.com", phone="081234567890"
        )

    def contact_url(self, action):
        return reverse(f"contacts:contact_{action}", args=[self.contact.pk])

    def test_list_and_empty_state(self):
        response = self.client.get(reverse("contacts:contact_list"))
        self.assertContains(response, "081234567890")
        self.assertContains(response, 'hx-swap="beforeend"')
        Contact.objects.all().delete()
        response = self.client.get(reverse("contacts:contact_list"))
        self.assertContains(response, "Tidak ada kontak.")

    def test_add_returns_only_new_row_and_out_of_band_feedback(self):
        response = self.client.post(
            reverse("contacts:contact_add"),
            {"name": "Budi", "email": "budi@example.com", "phone": "089876543210"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Contact.objects.filter(name="Budi", phone="089876543210").exists())
        self.assertContains(response, "Budi", status_code=201)
        self.assertNotContains(response, "ani@example.com", status_code=201)
        self.assertNotContains(response, "<html", status_code=201)
        self.assertContains(response, 'hx-swap-oob="true"', status_code=201)
        self.assertContains(response, 'hx-swap-oob="delete"', status_code=201)
        self.assertContains(response, "Kontak berhasil ditambahkan!", status_code=201)

    def test_invalid_add_does_not_save_or_report_success(self):
        response = self.client.post(
            reverse("contacts:contact_add"), {"name": "", "email": "invalid"}
        )
        self.assertEqual(Contact.objects.count(), 1)
        self.assertContains(response, 'id="feedback"')
        self.assertNotContains(response, "Kontak berhasil ditambahkan!")

    def test_search_is_case_insensitive_and_returns_partial(self):
        Contact.objects.create(name="Budi", email="budi@example.com")
        response = self.client.get(reverse("contacts:contact_search"), {"q": "ANI"})
        self.assertContains(response, "ani@example.com")
        self.assertNotContains(response, "budi@example.com")
        self.assertNotContains(response, "<html")
        response = self.client.get(reverse("contacts:contact_search"), {"q": "missing"})
        self.assertContains(response, "Tidak ada kontak.")
        response = self.client.get(reverse("contacts:contact_search"), {"q": ""})
        self.assertContains(response, "budi@example.com")

    def test_edit_returns_form_with_phone(self):
        response = self.client.get(self.contact_url("edit"))
        self.assertContains(response, 'hx-put=')
        self.assertContains(response, 'value="081234567890"')
        self.assertContains(response, f'form="edit-form-{self.contact.pk}"')

    def test_update_parses_put_body_and_returns_display_row(self):
        response = self.client.put(
            self.contact_url("update"),
            urlencode({"name": "Ani Baru", "email": "baru@example.com", "phone": "081111"}),
            content_type="application/x-www-form-urlencoded",
        )
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Ani Baru")
        self.assertEqual(self.contact.email, "baru@example.com")
        self.assertEqual(self.contact.phone, "081111")
        self.assertContains(response, "baru@example.com")
        self.assertNotContains(response, "<input")

    def test_invalid_update_preserves_saved_data_and_returns_edit_form(self):
        response = self.client.put(
            self.contact_url("update"),
            urlencode({"name": "Ani Baru", "email": "invalid", "phone": "081111"}),
            content_type="application/x-www-form-urlencoded",
        )
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Ani")
        self.assertContains(response, 'value="Ani Baru"')
        self.assertContains(response, 'class="errorlist"')

    def test_cancel_returns_saved_display_row(self):
        response = self.client.get(self.contact_url("row"))
        self.assertContains(response, "ani@example.com")
        self.assertNotContains(response, "<input")

    def test_delete_returns_empty_200_for_outer_html_swap(self):
        response = self.client.delete(self.contact_url("delete"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"")
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())

    def test_mutations_reject_wrong_methods(self):
        for url in [reverse("contacts:contact_add"), self.contact_url("update"), self.contact_url("delete")]:
            self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(self.contact_url("update")).status_code, 405)
        self.assertEqual(self.client.post(self.contact_url("delete")).status_code, 405)
        self.assertEqual(Contact.objects.count(), 1)

    def test_csrf_is_required_for_post_put_and_delete(self):
        client = Client(enforce_csrf_checks=True)
        client.get(reverse("contacts:contact_list"))
        self.assertEqual(client.post(reverse("contacts:contact_add"), {}).status_code, 403)
        self.assertEqual(client.put(self.contact_url("update"), "").status_code, 403)
        self.assertEqual(client.delete(self.contact_url("delete")).status_code, 403)
        token = client.cookies["csrftoken"].value
        response = client.put(
            self.contact_url("update"),
            urlencode({"name": "Ani", "email": "ani@example.com", "phone": "082222"}),
            content_type="application/x-www-form-urlencoded",
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, 200)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.phone, "082222")
        response = client.delete(self.contact_url("delete"), HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 200)

    def test_contact_text_is_escaped_in_display_and_edit_fragments(self):
        self.contact.name = '<script>alert("x")</script>'
        self.contact.save()
        for action in ["row", "edit"]:
            response = self.client.get(self.contact_url(action))
            self.assertContains(response, "&lt;script&gt;")
            self.assertNotContains(response, '<script>alert("x")</script>')
