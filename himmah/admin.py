from django.contrib import admin
from .models import Goal, Task, DayPlan, DayReview, WeekReview, Reflection, Distraction

admin.site.register(Goal)
admin.site.register(Task)
admin.site.register(DayPlan)
admin.site.register(DayReview)
admin.site.register(WeekReview)
admin.site.register(Reflection)
admin.site.register(Distraction)