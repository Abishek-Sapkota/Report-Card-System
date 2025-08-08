from celery import shared_task
from django.db.models import Avg, F
from .models import Mark, ReportCard
from .serializers import ReportCardSerializer


@shared_task
def calculate_student_overview(student, year):
    """
    Celery task to calculate student overview
    """
    qs = ReportCard.objects.filter(student=student, year=year).prefetch_related("marks__subject")
    cards_serializer = ReportCardSerializer(qs, many=True)

    marks_qs = Mark.objects.filter(report_card__student=student, report_card__year=year)
    subject_aggregate = (
        marks_qs
        .annotate(subject_name=F("subject__name"))
        .values("subject_name")
        .annotate(average_score=Avg("score")))
    overall_average = marks_qs.aggregate(overall_average=Avg("score"))["overall_average"]

    return {
        "report_cards": cards_serializer.data,
        "subject_averages": list(subject_aggregate),
        "overall_average": overall_average
    }
