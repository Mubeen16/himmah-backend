from django.contrib.auth.models import User
from himmah.models import Goal, DayPlan, Task
from datetime import date, time

u = User.objects.first()
print("Using user:", u.username)

brocamp = Goal.objects.create(user=u,title="Brocamp",category="engineering",status="active",is_primary=True,target_hours=400,start_date=date(2026,1,1),target_date=date(2026,10,1))
ddia = Goal.objects.create(user=u,title="DDIA Projects",category="engineering",status="active",is_primary=False,target_hours=200,start_date=date(2026,1,1),target_date=date(2026,10,1))
ml = Goal.objects.create(user=u,title="ML Algorithms",category="engineering",status="active",is_primary=False,target_hours=150,start_date=date(2026,1,1),target_date=date(2026,10,1))
print("Goals created")

today = date.today()
plan = DayPlan.objects.create(user=u,date=today,intention="today I go deep. no new ideas. just execute.",niyyah_for_allah="for Allah's sake",niyyah_for_self="building discipline",day_start_time=time(9,0))
print("Plan created:", plan.date)

Task.objects.create(user=u,goal=brocamp,day_plan=plan,title="Brocamp Week 1 — DRF serializers",scheduled_date=today,planned_start_time=time(9,0),planned_end_time=time(10,0),estimated_mins=60,order=1)
Task.objects.create(user=u,goal=ddia,day_plan=plan,title="DDIA Chapter 3 — storage engines",scheduled_date=today,planned_start_time=time(10,0),planned_end_time=time(11,0),estimated_mins=60,order=2)
Task.objects.create(user=u,goal=ml,day_plan=plan,title="ML Week 1 — linear regression",scheduled_date=today,planned_start_time=time(11,0),planned_end_time=time(12,30),estimated_mins=90,order=3)
print("Tasks created. Done.")
