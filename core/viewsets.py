from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from django.db.models import Avg

from .models import Student, Subject, ReportCard, Mark
from .serializers import (
    StudentModelSerializer, SubjectModelSerializer, ReportCardSerializer,
    MarkSerializer, AddMarkSerializer
)


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

    def perform_create(self, serializer):
        # Additional logic: e.g. prevent duplicate ReportCards for the same student/term/year
        serializer.save()


class MarkModelViewSet(DefaultAuthMixin, viewsets.ModelViewSet):
    queryset = Mark.objects.all().select_related("subject", "report_card")
    serializer_class = AddMarkSerializer

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return MarkSerializer
        return AddMarkSerializer


# Custom detailed and aggregate views

class ReportCardDetailAPI(DefaultAuthMixin, APIView):
    def get(self, request, pk):
        report_card = ReportCard.objects.select_related("student").prefetch_related("marks__subject").get(pk=pk)
        serializer = ReportCardSerializer(report_card)
        return Response(serializer.data)


class StudentYearlyReportCardsAPI(DefaultAuthMixin, APIView):
    """
    Retrieve all report cards for a student in a given year,
    with average score per subject and overall average for the year.
    ?year=<year>
    """

    def get(self, request, student_id):
        year = request.GET.get("year")
        qs = ReportCard.objects.filter(student_id=student_id, year=year).prefetch_related("marks__subject")
        cards_serializer = ReportCardSerializer(qs, many=True)

        # Compute averages efficiently
        marks_qs = Mark.objects.filter(report_card__student_id=student_id, report_card__year=year)
        subject_agg = marks_qs.values("subject__name").annotate(avg_score=Avg("score"))
        overall_avg = marks_qs.aggregate(overall_avg=Avg("score"))["overall_avg"]

        return Response({
            "report_cards": cards_serializer.data,
            "subject_averages": list(subject_agg),
            "overall_average": overall_avg
        })
