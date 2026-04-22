from django.urls import include, path
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

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
    health_check,
    request_password_reset,
    register,
)


class RateLimitedTokenView(TokenObtainPairView):
    @method_decorator(ratelimit(key="ip", rate="10/m", block=True))
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("token/", RateLimitedTokenView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", register, name="register"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("health/", health_check, name="health_check"),
    path("auth/password-reset/", request_password_reset, name="request_password_reset"),
    path("auth/password-reset/confirm/", confirm_password_reset, name="confirm_password_reset"),
    path("", include(router.urls)),
]
