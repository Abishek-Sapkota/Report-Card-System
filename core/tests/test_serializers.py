from django.test import TestCase
from decimal import Decimal
from .models import Student, Subject, ReportCard, Mark
from .serializers import (
    StudentModelSerializer,
    SubjectModelSerializer,
    ReportCardModelSerializer,
    MarkModelSerializer,
    MarkSerializer,
    ReportCardSerializer,
    AddMarkSerializer,
)
from rest_framework.exceptions import ValidationError


class StudentSerializerTest(TestCase):
    def test_serialize_student(self):
        student = Student.objects.create(name="Alice", email="alice@example.com")
        serializer = StudentModelSerializer(student)
        data = serializer.data
        self.assertEqual(data["name"], "Alice")
        self.assertEqual(data["email"], "alice@example.com")
        self.assertIn("id", data)

    def test_deserialize_student_valid(self):
        data = {"name": "Bob", "email": "bob@example.com"}
        serializer = StudentModelSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)


class SubjectSerializerTest(TestCase):
    def test_serialize_subject(self):
        subject = Subject.objects.create(name="Math", code="MATH")
        serializer = SubjectModelSerializer(subject)
        data = serializer.data
        self.assertEqual(data["name"], "Math")
        self.assertEqual(data["code"], "MATH")

    def test_deserialize_subject_valid(self):
        data = {"name": "Science", "code": "SCI"}
        serializer = SubjectModelSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)


class ReportCardModelSerializerTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(name="Carl", email="carl@example.com")

    def test_serialize_report_card(self):
        rc = ReportCard.objects.create(student=self.student, term="Fall", year="2023")
        serializer = ReportCardModelSerializer(rc)
        data = serializer.data
        self.assertEqual(data["term"], "Fall")
        self.assertEqual(data["year"], "2023")
        self.assertEqual(data["student"], self.student.id)

    def test_deserialize_report_card_valid(self):
        data = {"student": self.student.id, "term": "Spring", "year": "2024"}
        serializer = ReportCardModelSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_deserialize_report_card_duplicate(self):
        # Create first report card
        ReportCard.objects.create(student=self.student, term="Fall", year="2023")
        data = {"student": self.student.id, "term": "fall", "year": "2023"}  # Case-insensitive term

        serializer = ReportCardSerializer(data=data)  # Note: uses ReportCardSerializer (has validate)
        with self.assertRaises(ValidationError) as cm:
            serializer.is_valid(raise_exception=True)
        self.assertIn("already exists", str(cm.exception))


class MarkModelSerializerTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(name="Dana", email="dana@example.com")
        self.subject = Subject.objects.create(name="History", code="HIST")
        self.report_card = ReportCard.objects.create(student=self.student, term="Winter", year="2023")

    def test_serialize_mark(self):
        mark = Mark.objects.create(report_card=self.report_card, subject=self.subject, score=Decimal("78.5"))
        serializer = MarkModelSerializer(mark)
        data = serializer.data
        self.assertEqual(data["score"], "78.5")
        self.assertEqual(data["subject"], self.subject.id)
        self.assertEqual(data["report_card"], self.report_card.id)

    def test_deserialize_mark_valid(self):
        data = {
            "report_card": self.report_card.id,
            "subject": self.subject.id,
            "score": "88.0"
        }
        serializer = MarkModelSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)


class MarkSerializerTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(name="Eve", email="eve@example.com")
        self.subject = Subject.objects.create(name="Geography", code="GEO")
        self.report_card = ReportCard.objects.create(student=self.student, term="Summer", year="2023")
        self.mark = Mark.objects.create(report_card=self.report_card, subject=self.subject, score=Decimal("92.0"))

    def test_mark_serializer_includes_subject_detail(self):
        serializer = MarkSerializer(self.mark)
        data = serializer.data
        self.assertEqual(data["score"], "92.0")
        self.assertIn("subject_detail", data)
        self.assertEqual(data["subject_detail"]["name"], "Geography")


class ReportCardSerializerTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(name="Frank", email="frank@example.com")
        self.subject = Subject.objects.create(name="Physics", code="PHY")
        self.report_card = ReportCard.objects.create(student=self.student, term="Fall", year="2023")
        self.mark = Mark.objects.create(report_card=self.report_card, subject=self.subject, score=Decimal("85"))

    def test_report_card_serializer_includes_nested(self):
        serializer = ReportCardSerializer(self.report_card)
        data = serializer.data
        self.assertEqual(data["term"], "Fall")
        self.assertEqual(data["student_detail"]["name"], "Frank")
        self.assertEqual(len(data["marks"]), 1)
        self.assertEqual(data["marks"][0]["score"], "85")


class AddMarkSerializerTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(name="Gina", email="gina@example.com")
        self.subject = Subject.objects.create(name="Chemistry", code="CHEM")
        self.report_card = ReportCard.objects.create(student=self.student, term="Spring", year="2024")

    def test_add_mark_serializer_valid(self):
        data = {
            "report_card": self.report_card.id,
            "subject": self.subject.id,
            "score": "79.5"
        }
        serializer = AddMarkSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_add_mark_serializer_missing_fields(self):
        data = {"score": "79.5"}  # Missing report_card and subject
        serializer = AddMarkSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("report_card", serializer.errors)
        self.assertIn("subject", serializer.errors)
