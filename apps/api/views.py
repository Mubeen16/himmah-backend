import logging
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_ratelimit.decorators import ratelimit
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from himmah.models import (
    DayIntention,
    DayPlan,
    DayReview,
    Distraction,
    Goal,
    Reflection,
    Task,
    TaskReflection,
    WeekReview,
)

from .serializers import (
    DayIntentionSerializer,
    DayPlanSerializer,
    DayReviewSerializer,
    DistractionSerializer,
    GoalSerializer,
    ReflectionSerializer,
    TaskReflectionSerializer,
    TaskSerializer,
    WeekReviewSerializer,
)

logger = logging.getLogger(__name__)


class GoalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer

    def get_queryset(self):
        queryset = Goal.objects.filter(user=self.request.user)
        is_primary = self.request.query_params.get("is_primary")
        status = self.request.query_params.get("status")
        if is_primary is not None:
            queryset = queryset.filter(is_primary=is_primary.lower() == "true")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user).select_related("goal")
        date = self.request.query_params.get("date")
        start = self.request.query_params.get("start")
        end = self.request.query_params.get("end")
        if date:
            queryset = queryset.filter(scheduled_date=date)
        if start and end:
            queryset = queryset.filter(scheduled_date__range=[start, end])
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def start_timer(self, request, pk=None):
        task = self.get_object()
        task.timer_started_at = timezone.now()
        task.save()
        return Response({"status": "timer started"})

    @action(detail=True, methods=["post"])
    def stop_timer(self, request, pk=None):
        task = self.get_object()
        if task.timer_started_at:
            task.timer_ended_at = timezone.now()
            diff = task.timer_ended_at - task.timer_started_at
            task.actual_mins = int(diff.total_seconds() / 60)
            task.save()
        return Response({"status": "timer stopped", "actual_mins": task.actual_mins})

    @action(detail=True, methods=["post"])
    def mark_done(self, request, pk=None):
        task = self.get_object()
        task.done = True
        task.done_at = timezone.now()
        task.save()
        return Response({"status": "task marked done"})


class DayPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DayPlanSerializer

    def get_queryset(self):
        queryset = DayPlan.objects.filter(user=self.request.user)
        date = self.request.query_params.get("date")
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DayIntentionViewSet(viewsets.ModelViewSet):
    serializer_class = DayIntentionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = DayIntention.objects.filter(user=self.request.user)
        date = self.request.query_params.get("date")
        if date:
            qs = qs.filter(date=date)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DayReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DayReviewSerializer

    def get_queryset(self):
        return DayReview.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WeekReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = WeekReviewSerializer

    def get_queryset(self):
        return WeekReview.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReflectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ReflectionSerializer

    def get_queryset(self):
        return Reflection.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskReflectionViewSet(viewsets.ModelViewSet):
    serializer_class = TaskReflectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = TaskReflection.objects.filter(user=self.request.user)
        task_id = self.request.query_params.get("task")
        if task_id:
            qs = qs.filter(task_id=task_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DistractionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DistractionSerializer

    def get_queryset(self):
        qs = Distraction.objects.filter(user=self.request.user)
        verdict = self.request.query_params.get("verdict")
        pending = self.request.query_params.get("pending")
        if verdict == "none":
            qs = qs.filter(verdict__isnull=True)
        elif verdict:
            qs = qs.filter(verdict=verdict)
        if pending == "true":
            qs = qs.filter(verdict__isnull=True)
        return qs.order_by("-triggered_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["POST"])
@permission_classes([AllowAny])
@ratelimit(key="ip", rate="5/m", block=True)
def register(request):
    username = request.data.get("username", "").strip()
    email = request.data.get("email", "").strip()
    password = request.data.get("password", "")

    if not username or not password:
        return Response(
            {"error": "username and password required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(password) < 8:
        return Response(
            {"error": "password must be at least 8 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "username already taken"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if email and User.objects.filter(email=email).exists():
        return Response(
            {"error": "email already registered"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get("email", "").strip()
    if not email:
        return Response(
            {"error": "email is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        # Percent-encode query values so "=" in tokens / uids is not confused with MIME
        # quoted-printable line breaks when reading the console email in Docker logs.
        base = settings.FRONTEND_URL.rstrip("/")
        reset_url = f"{base}/reset-password?{urlencode({'uid': uid, 'token': token})}"
        body = (
            f"Click this link to reset your password:\n\n{reset_url}\n\n"
            "This link expires in 24 hours.\n\n"
            "If you did not request this, ignore this email."
        )
        if settings.DEBUG:
            body += (
                "\n\n(Development: console email can wrap long links. If the link fails, "
                "copy the single line from the server log that starts with PASSWORD_RESET_URL=.)"
            )
        send_mail(
            subject="Reset your Himmah password",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        if settings.DEBUG:
            # Console email wraps long URLs; copy this single line for a reliable reset link.
            logger.warning("PASSWORD_RESET_URL=%s", reset_url)
    except User.DoesNotExist:
        pass
    return Response(
        {"message": "if an account exists with that email, a reset link has been sent"},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def confirm_password_reset(request):
    uid = (request.data.get("uid") or "").strip()
    token = (request.data.get("token") or "").strip()
    password = request.data.get("password", "")

    if not uid or not token or not password:
        return Response(
            {"error": "uid, token and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if len(password) < 8:
        return Response(
            {"error": "password must be at least 8 characters"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
    except (User.DoesNotExist, ValueError, TypeError):
        return Response(
            {"error": "invalid reset link"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not default_token_generator.check_token(user, token):
        return Response(
            {"error": "reset link has expired or is invalid"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user.set_password(password)
    user.save()
    return Response(
        {"message": "password reset successfully"},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    return Response({"status": "ok"})
