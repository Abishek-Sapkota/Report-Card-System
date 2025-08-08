from django.test import TestCase
from .models import Student, Subject, ReportCard, Mark


class StudentModelTest(TestCase):
    def test_total_value(self):
        product = Student.objects.create(name="test student", email="teststudent@gmail.com", date_of_birth="2000-12-10")
        self.assertEqual(product.name, "test student")
        self.assertEqual(product.email, "teststudent@gmail.com")
        self.assertEqual(product.date_of_birth, "2000-12-10")
