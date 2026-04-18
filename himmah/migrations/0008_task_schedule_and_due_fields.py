from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("himmah", "0007_task_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="due_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="is_all_day",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="task",
            name="planned_end_time",
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="planned_start_time",
            field=models.TimeField(blank=True, null=True),
        ),
    ]
