import pytest
from decimal import Decimal
from django.db import IntegrityError

from core.models import Student, Subject, ReportCard, Mark


@pytest.mark.django_db
class TestStudentModel:

    def test_create_student(self):
        student = Student.objects.create(
            name="John Doe",
            email="john@example.com",
            date_of_birth="2000-01-01"
        )
        assert student.id is not None
        assert student.name == "John Doe"


@pytest.mark.django_db
class TestSubjectModel:

    def test_create_subject(self):
        subject = Subject.objects.create(
            name="Mathematics",
            code="MAT"
        )
        assert subject.id is not None
        assert subject.code == "MAT"
        assert str(subject) == "Mathematics"


@pytest.mark.django_db
class TestReportCardModel:

    def test_create_report_card(self):
        student = Student.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            date_of_birth="2001-05-15"
        )
        report_card = ReportCard.objects.create(
            student=student,
            term="Term1",
            year=2024
        )
        assert report_card.id is not None
        assert report_card.student == student


@pytest.mark.django_db
class TestMarkModel:

    def test_create_mark(self):
        student = Student.objects.create(
            name="Alice",
            email="alice@example.com",
            date_of_birth="2002-03-10"
        )
        subject = Subject.objects.create(name="Science", code="SCI101")
        report_card = ReportCard.objects.create(
            student=student,
            term="Term2",
            year=2025
        )
        mark = Mark.objects.create(
            report_card=report_card,
            subject=subject,
            score=Decimal("85.50")
        )
        assert mark.id is not None
        assert mark.score == Decimal("85.50")

    def test_unique_mark_subject_constraint(self):
        student = Student.objects.create(
            name="Bob",
            email="bob@example.com",
            date_of_birth="2003-07-20"
        )
        subject = Subject.objects.create(name="History", code="HIS101")
        report_card = ReportCard.objects.create(
            student=student,
            term="Term3",
            year=2025
        )
        Mark.objects.create(
            report_card=report_card,
            subject=subject,
            score=Decimal("70.00")
        )

        with pytest.raises(IntegrityError):
            Mark.objects.create(
                report_card=report_card,
                subject=subject,
                score=Decimal("75.00")
            )
