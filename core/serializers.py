from rest_framework import serializers
from .models import Student, Subject, ReportCard, Mark


class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "name", "email", "date_of_birth"]
        extra_kwargs = {
            "id": {"read_only": True},
        }


class SubjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "code",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }


class ReportCardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportCard
        fields = [
            "id",
            "student",
            "term",
            "year",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }


class MarkModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = [
            "id",
            "report_card",
            "subject",
            "score",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }


class MarkSerializer(serializers.ModelSerializer):
    subject = SubjectModelSerializer(read_only=True)

    class Meta:
        model = Mark
        fields = ["id", "score", "subject"]


class ReportCardSerializer(serializers.ModelSerializer):
    marks = MarkSerializer(many=True, read_only=True)
    student_detail = StudentModelSerializer(source="student", read_only=True)

    class Meta:
        model = ReportCard
        fields = ["id", "student", "term", "year", "marks", "student_detail"]

    def validate(self, data):
        student = data.get("student")
        term = data.get("term")
        year = data.get("year")
        if ReportCard.objects.filter(student=student, term__iexact=term, year=year).exists():
            raise serializers.ValidationError(f"Report card for this student for {term} {year} already exists")
        return data


class AddMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mark
        fields = [
            "id",
            "subject",
            "report_card",
            "score"
        ]
    extra_kwargs = {
        "id": {"read_only": True},
    }
