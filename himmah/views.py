from django.contrib.auth.models import User
from django_ratelimit.decorators import ratelimit
from django.utils import timezone
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
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
        date = self.request.query_params.get('date')
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
        queryset = Distraction.objects.filter(user=self.request.user)
        verdict = self.request.query_params.get("verdict")
        if verdict:
            queryset = queryset.filter(verdict=verdict)
        return queryset

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
