from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    StudentModelViewSet, SubjectModelViewSet, ReportCardModelViewSet, MarkModelViewSet,
    ReportCardDetailAPI, StudentYearlyReportCardsAPI
)

router = DefaultRouter()
router.register(r"students", StudentModelViewSet)
router.register(r"subjects", SubjectModelViewSet)
router.register(r"report-cards", ReportCardModelViewSet)
router.register(r"marks", MarkModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("report-card/<int:pk>/", ReportCardDetailAPI.as_view(), name="report-card-detail"),
    path("student/<int:student_id>/year-report-cards/", StudentYearlyReportCardsAPI.as_view(),
         name="student-yearly-report-cards")
]
