from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("himmah", "0006_dayplan_day_start_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="description",
            field=models.TextField(blank=True, default=""),
            preserve_default=False,
        ),
    ]
