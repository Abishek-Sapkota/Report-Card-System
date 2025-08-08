from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User
from decimal import Decimal
from core.models import Student, Subject, ReportCard, Mark


class BaseViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass1234")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)


class StudentViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp()
        self.student = Student.objects.create(name="John Doe", email="john@example.com", date_of_birth="1990-01-01")

    def test_list_students(self):
        url = reverse("student-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(s["id"] == self.student.id for s in response.data))

    def test_search_students(self):
        url = reverse("student-list") + "?search=John"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_avg_overview_without_year(self):
        url = reverse("student-avg-overview", kwargs={"pk": self.student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("message", response.data)

    def test_avg_overview_with_year(self):
        sub_math = Subject.objects.create(name="Math", code="MAT")
        sub_phy = Subject.objects.create(name="Physics", code="PSY")
        report_card = ReportCard.objects.create(student=self.student, year="2023", term="Fall")
        Mark.objects.create(report_card=report_card, subject=sub_math, score=Decimal("80"))
        Mark.objects.create(report_card=report_card, subject=sub_phy, score=Decimal("90"))

        url = reverse("student-avg-overview", kwargs={"pk": self.student.id}) + "?year=2023"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("report_cards", response.data)
        self.assertIn("subject_averages", response.data)
        self.assertIn("overall_average", response.data)
        self.assertEqual(len(response.data["report_cards"]), 1)
        self.assertEqual(len(response.data["subject_averages"]), 2)
        self.assertAlmostEqual(float(response.data["overall_average"]), 85.0)


class SubjectViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp()
        self.subject = Subject.objects.create(name="Science", code="SCI")

    def test_list_subjects(self):
        url = reverse("subject-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(s["id"] == self.subject.id for s in response.data))

    def test_search_subjects(self):
        url = reverse("subject-list") + "?search=Science"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class ReportCardViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp()
        self.student = Student.objects.create(name="Alice", email="alice@example.com", date_of_birth="1999-01-01")
        self.report_card = ReportCard.objects.create(student=self.student, year="2023", term="Fall")

    def test_list_report_cards(self):
        url = reverse("report-card-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(rc["id"] == self.report_card.id for rc in response.data))

    def test_filter_report_cards_by_student(self):
        url = reverse("report-card-list") + f"?student={self.student.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(rc["student"] == self.student.id for rc in response.data))


class MarkViewSetTest(BaseViewSetTest):
    def setUp(self):
        super().setUp()
        self.student = Student.objects.create(name="Bob", email="bob@example.com", date_of_birth="1999-01-01")
        self.subject = Subject.objects.create(name="History", code="HIST")
        self.another_subject = Subject.objects.create(name="Maths", code="MAT")
        self.report_card = ReportCard.objects.create(student=self.student, year="2023", term="Spring")
        self.mark = Mark.objects.create(report_card=self.report_card, subject=self.subject, score=Decimal("75"))

    def test_list_marks(self):
        url = reverse("mark-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(m["id"] == self.mark.id for m in response.data))

    def test_retrieve_mark(self):
        url = reverse("mark-detail", kwargs={"pk": self.mark.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.mark.id)

    def test_create_mark(self):
        url = reverse("mark-list")
        data = {
            "report_card": self.report_card.id,
            "subject": self.another_subject.id,
            "score": "85"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mark.objects.count(), 2)

    def test_update_mark(self):
        url = reverse("mark-detail", kwargs={"pk": self.mark.id})
        data = {"score": "90"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.mark.refresh_from_db()
        self.assertEqual(self.mark.score, Decimal(90))
