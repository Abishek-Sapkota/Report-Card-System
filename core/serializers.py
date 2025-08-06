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
    subject_detail = SubjectModelSerializer(source="subject", read_only=True)

    class Meta:
        model = Mark
        fields = ["id", "subject", "score", "subject_detail"]


class ReportCardSerializer(serializers.ModelSerializer):
    marks = MarkSerializer(many=True, read_only=True)
    student_detail = StudentModelSerializer(source="student", read_only=True)

    class Meta:
        model = ReportCard
        fields = ["id", "student", "term", "year", "marks", "student_detail"]


class AddMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = "__all__"
