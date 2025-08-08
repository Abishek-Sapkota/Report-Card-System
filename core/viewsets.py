from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.db.models import Avg, F

from .models import Student, Subject, ReportCard, Mark
from .serializers import (
    StudentModelSerializer, SubjectModelSerializer, ReportCardSerializer,
    MarkSerializer, AddMarkSerializer
)
from .tasks import calculate_student_overview


class DefaultAuthMixin:
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class StudentModelViewSet(DefaultAuthMixin, viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ["name", "email"]

    @action(detail=True, methods=["GET"], url_name="avg-overview", url_path="avg-overview")
    def avg_overview(self, request, pk=None):
        """
        Retrieve all report cards for a student in a given year,
        with average score per subject and overall average for the year.
        ?year=<year>
        """
        year = request.GET.get("year")
        if not year:
            from rest_framework import status
            return Response({"message": "Year is required to filter data!!"}, status=status.HTTP_400_BAD_REQUEST)
        student = self.get_object()
        overview_dict = calculate_student_overview.delay(student.pk, year)
        qs = ReportCard.objects.filter(student=student, year=year).prefetch_related("marks__subject")
        cards_serializer = ReportCardSerializer(qs, many=True)

        marks_qs = Mark.objects.filter(report_card__student=student, report_card__year=year)
        subject_aggregate = (
            marks_qs
            .annotate(subject_name=F("subject__name"))
            .values("subject_name")
            .annotate(average_score=Avg("score")))
        overall_average = marks_qs.aggregate(overall_average=Avg("score"))["overall_average"]

        return Response({
            "report_cards": cards_serializer.data,
            "subject_averages": list(subject_aggregate),
            "overall_average": overall_average
        })


class SubjectModelViewSet(DefaultAuthMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ["name", "code"]


class ReportCardModelViewSet(DefaultAuthMixin, viewsets.ModelViewSet):
    queryset = ReportCard.objects.all().select_related("student").prefetch_related("marks__subject")
    serializer_class = ReportCardSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_fields = ["student"]
    search_fields = ["term"]


class MarkModelViewSet(DefaultAuthMixin, viewsets.ModelViewSet):
    queryset = Mark.objects.all().select_related("subject", "report_card")
    serializer_class = AddMarkSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MarkSerializer
        return AddMarkSerializer
