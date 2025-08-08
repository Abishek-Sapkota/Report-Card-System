from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class ReportCard(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, db_index=True)
    term = models.CharField(max_length=100, db_index=True)
    year = models.IntegerField(db_index=True)

    def __str__(self):
        return f"{self.student.name}-{self.term}-{self.year}"


class Mark(models.Model):
    report_card = models.ForeignKey(
        ReportCard, on_delete=models.CASCADE, related_name="marks", db_index=True
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, db_index=True)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "report_card",
                    "subject"
                ],
                name="unique_mark_subject"
            )
        ]

    def __str__(self):
        return f"{self.subject}-{self.score}"
