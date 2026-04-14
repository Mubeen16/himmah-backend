from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    DayPlan,
    DayReview,
    Distraction,
    Goal,
    Reflection,
    Task,
    WeekReview,
)

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("email already exists")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )


class GoalSerializer(serializers.ModelSerializer):
    logged_hours = serializers.SerializerMethodField()
    child_goals = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = [
            "id",
            "title",
            "category",
            "status",
            "is_primary",
            "parent_goal",
            "target_hours",
            "logged_hours",
            "start_date",
            "target_date",
            "created_at",
            "updated_at",
            "child_goals",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "logged_hours"]

    def get_logged_hours(self, obj):
        return obj.logged_hours()

    def get_child_goals(self, obj):
        return GoalSerializer(obj.child_goals.all(), many=True).data


class ReflectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reflection
        fields = [
            "id",
            "task",
            "note",
            "what_went_well",
            "what_missed",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class GoalMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ["id", "title", "category"]


class TaskSerializer(serializers.ModelSerializer):
    reflection = ReflectionSerializer(read_only=True)
    goal_detail = GoalMinimalSerializer(source="goal", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "goal",
            "goal_detail",
            "day_plan",
            "title",
            "scheduled_date",
            "order",
            "estimated_mins",
            "actual_mins",
            "timer_started_at",
            "timer_ended_at",
            "done",
            "done_at",
            "skipped",
            "skip_reason",
            "reflection",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class DayPlanSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = DayPlan
        fields = [
            "id",
            "date",
            "intention",
            "niyyah_for_allah",
            "niyyah_for_self",
            "morning_energy",
            "morning_clarity",
            "sleep_quality",
            "tasks",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class DayReviewSerializer(serializers.ModelSerializer):
    completed_count = serializers.SerializerMethodField()
    total_count = serializers.SerializerMethodField()

    class Meta:
        model = DayReview
        fields = [
            "id",
            "date",
            "score",
            "reflection",
            "energy_level",
            "distracted_by",
            "gratitude_note",
            "barakah_felt",
            "barakah_note",
            "completed_count",
            "total_count",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_completed_count(self, obj):
        return obj.completed_count()

    def get_total_count(self, obj):
        return obj.total_count()


class WeekReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekReview
        fields = [
            "id",
            "week_start",
            "week_end",
            "score",
            "what_worked",
            "what_didnt",
            "focus_next_week",
            "average_energy",
            "average_score",
            "best_day",
            "worst_day",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class DistractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distraction
        fields = [
            "id",
            "goal",
            "title",
            "description",
            "triggered_at",
            "verdict",
            "verdict_reason",
            "reviewed_at",
            "revisit_after",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
