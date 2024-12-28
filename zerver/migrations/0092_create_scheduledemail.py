# Generated by Django 1.11.2 on 2017-07-11 23:41
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zerver", "0091_realm_allow_edit_history"),
    ]

    operations = [
        migrations.CreateModel(
            name="ScheduledEmail",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("scheduled_timestamp", models.DateTimeField(db_index=True)),
                ("data", models.TextField()),
                ("address", models.EmailField(db_index=True, max_length=254, null=True)),
                ("type", models.PositiveSmallIntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.DeleteModel(
            name="ScheduledJob",
        ),
    ]
