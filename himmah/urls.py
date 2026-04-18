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
    path("", include(router.urls)),
]
