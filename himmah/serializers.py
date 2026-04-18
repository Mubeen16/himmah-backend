from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

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


class TaskReflectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskReflection
        fields = [
            "id",
            "task",
            "note",
            "what_went_well",
            "what_missed",
            "actual_mins",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class GoalMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ["id", "title", "category", "is_primary"]


class TaskSerializer(serializers.ModelSerializer):
    """Reflection is optional reverse OneToOne — direct nested access raises if missing."""

    reflection = serializers.SerializerMethodField()
    task_reflection = TaskReflectionSerializer(read_only=True, allow_null=True)
    goal_detail = GoalMinimalSerializer(source="goal", read_only=True, allow_null=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "goal",
            "goal_detail",
            "day_plan",
            "title",
            "description",
            "scheduled_date",
            "planned_start_time",
            "planned_end_time",
            "is_all_day",
            "due_date",
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
            "task_reflection",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        # On partial updates, distinguish "key omitted" from "explicit null" (e.g. clearing times for all-day).
        if self.instance is not None:
            if "is_all_day" in attrs:
                is_all_day = attrs.get("is_all_day")
            else:
                is_all_day = self.instance.is_all_day
            if "planned_start_time" in attrs:
                start_time = attrs.get("planned_start_time")
            else:
                start_time = self.instance.planned_start_time
            if "planned_end_time" in attrs:
                end_time = attrs.get("planned_end_time")
            else:
                end_time = self.instance.planned_end_time
            if "goal" in attrs:
                goal = attrs.get("goal")
            else:
                goal = self.instance.goal
        else:
            is_all_day = attrs["is_all_day"] if "is_all_day" in attrs else False
            start_time = attrs.get("planned_start_time")
            end_time = attrs.get("planned_end_time")
            goal = attrs.get("goal")

        if goal is None:
            raise serializers.ValidationError({"goal": "goal is required for every task"})

        if is_all_day and (start_time is not None or end_time is not None):
            raise serializers.ValidationError(
                {"planned_start_time": "all-day tasks cannot have start or end times"}
            )

        if not is_all_day and ((start_time is None) != (end_time is None)):
            raise serializers.ValidationError(
                {"planned_end_time": "provide both start and end times, or leave both empty"}
            )

        if start_time is not None and end_time is not None and end_time <= start_time:
            raise serializers.ValidationError(
                {"planned_end_time": "end time must be after start time"}
            )

        return attrs

    def get_reflection(self, obj):
        try:
            return ReflectionSerializer(obj.reflection).data
        except ObjectDoesNotExist:
            return None


class DayIntentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayIntention
        fields = [
            'id',
            'day_plan',
            'date',
            'title',
            'focus',
            'purpose',
            'character',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


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
            "day_start_time",
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
