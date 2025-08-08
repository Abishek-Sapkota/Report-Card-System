from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import (
    StudentModelViewSet, SubjectModelViewSet, ReportCardModelViewSet, MarkModelViewSet
)

router = DefaultRouter()
router.register(r"students", StudentModelViewSet)
router.register(r"subjects", SubjectModelViewSet)
router.register(r"report-cards", ReportCardModelViewSet)
router.register(r"marks", MarkModelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
