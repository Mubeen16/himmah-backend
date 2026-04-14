from datetime import timedelta

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Goal(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
        ('pivoted', 'Pivoted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_primary = models.BooleanField(default=False)
    parent_goal = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='child_goals')
    target_hours = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField()
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def logged_hours(self):
        from django.db.models import Sum
        result = self.tasks.filter(done=True).aggregate(total=Sum('actual_mins'))
        total_mins = result['total'] or 0
        return round(total_mins / 60, 2)

    def __str__(self):
        return self.title


class DayPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='day_plans')
    date = models.DateField()
    intention = models.TextField(blank=True)
    niyyah_for_allah = models.TextField(blank=True)
    niyyah_for_self = models.TextField(blank=True)
    morning_energy = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    morning_clarity = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    sleep_quality = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user} — {self.date}"


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    day_plan = models.ForeignKey(DayPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=255)
    scheduled_date = models.DateField()
    order = models.PositiveIntegerField(default=0)
    estimated_mins = models.PositiveIntegerField()
    actual_mins = models.PositiveIntegerField(null=True, blank=True)
    timer_started_at = models.DateTimeField(null=True, blank=True)
    timer_ended_at = models.DateTimeField(null=True, blank=True)
    done = models.BooleanField(default=False)
    done_at = models.DateTimeField(null=True, blank=True)
    skipped = models.BooleanField(default=False)
    skip_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Reflection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reflections')
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='reflection')
    note = models.TextField(blank=True)
    what_went_well = models.TextField(blank=True)
    what_missed = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reflection — {self.task.title}"


class DayReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='day_reviews')
    date = models.DateField()
    score = models.PositiveSmallIntegerField()
    reflection = models.TextField(blank=True)
    energy_level = models.PositiveSmallIntegerField()
    distracted_by = models.TextField(blank=True)
    gratitude_note = models.TextField(blank=True)
    barakah_felt = models.BooleanField(default=False)
    barakah_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')

    def completed_count(self):
        return Task.objects.filter(user=self.user, scheduled_date=self.date, done=True).count()

    def total_count(self):
        return Task.objects.filter(user=self.user, scheduled_date=self.date).count()

    def __str__(self):
        return f"Review — {self.date}"


class Weekday(models.IntegerChoices):
    MONDAY = 0, "Monday"
    TUESDAY = 1, "Tuesday"
    WEDNESDAY = 2, "Wednesday"
    THURSDAY = 3, "Thursday"
    FRIDAY = 4, "Friday"
    SATURDAY = 5, "Saturday"
    SUNDAY = 6, "Sunday"


class WeekReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='week_reviews')
    week_start = models.DateField()
    week_end = models.DateField()
    score = models.PositiveSmallIntegerField()
    what_worked = models.TextField(blank=True)
    what_didnt = models.TextField(blank=True)
    focus_next_week = models.TextField(blank=True)
    average_energy = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    average_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    best_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=Weekday.choices,
    )
    worst_day = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=Weekday.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'week_start')

    def __str__(self):
        return f"Week Review — {self.week_start}"


class Distraction(models.Model):
    VERDICT_CHOICES = [
        ('parked', 'Parked'),
        ('pivot', 'Pivot'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='distractions')
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True, related_name='distractions')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    triggered_at = models.DateTimeField()
    verdict = models.CharField(max_length=20, choices=VERDICT_CHOICES, null=True, blank=True)
    verdict_reason = models.TextField(blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    revisit_after = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self._state.adding and self.revisit_after is None and self.triggered_at is not None:
            self.revisit_after = (self.triggered_at + timedelta(hours=48)).date()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title