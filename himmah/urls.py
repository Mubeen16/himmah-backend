from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DayIntentionViewSet,
    DayPlanViewSet,
    DayReviewViewSet,
    DistractionViewSet,
    GoalViewSet,
    ReflectionViewSet,
    TaskReflectionViewSet,
    TaskViewSet,
    WeekReviewViewSet,
    confirm_password_reset,
    request_password_reset,
)

router = DefaultRouter()
router.register(r"goals", GoalViewSet, basename="goal")
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"dayplans", DayPlanViewSet, basename="dayplan")
router.register(r"dayintentions", DayIntentionViewSet, basename="dayintention")
router.register(r"dayreviews", DayReviewViewSet, basename="dayreview")
router.register(r"weekreviews", WeekReviewViewSet, basename="weekreview")
router.register(r"reflections", ReflectionViewSet, basename="reflection")
router.register(r"taskreflections", TaskReflectionViewSet, basename="taskreflection")
router.register(r"distractions", DistractionViewSet, basename="distraction")

urlpatterns = [
    path("auth/password-reset/", request_password_reset, name="request_password_reset"),
    path("auth/password-reset/confirm/", confirm_password_reset, name="confirm_password_reset"),
    path("", include(router.urls)),
]
