from django.test import TestCase
from django.urls import reverse

from .models import Application, Job, User


class JobPortalTests(TestCase):
    def setUp(self):
        self.employer = User.objects.create_user(
            username="company", password="test-pass-123", role=User.Role.EMPLOYER
        )
        self.seeker = User.objects.create_user(
            username="candidate", password="test-pass-123", role=User.Role.SEEKER
        )
        self.job = Job.objects.create(
            employer=self.employer,
            title="Python Developer",
            company="Green Company",
            description="Build useful software.",
            location="Remote",
            category="Engineering",
        )

    def test_job_search_filters_by_location_category_and_company(self):
        response = self.client.get(
            reverse("job_list"),
            {"location": "remote", "category": "engineer", "company": "green"},
        )
        self.assertContains(response, "Python Developer")

        response = self.client.get(reverse("job_list"), {"location": "London"})
        self.assertNotContains(response, "Python Developer")

    def test_job_seeker_can_apply_once(self):
        self.client.force_login(self.seeker)
        response = self.client.post(reverse("job_detail", args=[self.job.pk]), {"cover_letter": "Hello!"})
        self.assertRedirects(response, reverse("job_detail", args=[self.job.pk]))
        self.assertEqual(Application.objects.filter(job=self.job, applicant=self.seeker).count(), 1)

        self.client.post(reverse("job_detail", args=[self.job.pk]), {"cover_letter": "Again"})
        self.assertEqual(Application.objects.filter(job=self.job, applicant=self.seeker).count(), 1)

    def test_employer_cannot_edit_another_employers_listing(self):
        another_employer = User.objects.create_user(
            username="other-company", password="test-pass-123", role=User.Role.EMPLOYER
        )
        self.client.force_login(another_employer)
        response = self.client.get(reverse("job_edit", args=[self.job.pk]))
        self.assertEqual(response.status_code, 404)
