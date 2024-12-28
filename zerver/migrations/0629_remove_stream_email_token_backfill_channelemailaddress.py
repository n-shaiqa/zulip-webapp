# Generated by Django 5.0.9 on 2024-11-21 12:58

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import connection, migrations, models
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps
from psycopg2.sql import SQL

from zerver.models.streams import generate_email_token_for_stream


def backfill_channelemailaddress(apps: StateApps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    UserProfile = apps.get_model("zerver", "UserProfile")

    with connection.cursor() as cursor:
        cursor.execute(SQL("SELECT MAX(id) FROM zerver_stream;"))
        (max_id,) = cursor.fetchone()

    if max_id is None:
        return

    BATCH_SIZE = 10000
    max_id += BATCH_SIZE / 2
    lower_id_bound = 0
    mail_gateway_bot_id = UserProfile.objects.get(email__iexact=settings.EMAIL_GATEWAY_BOT).id
    while lower_id_bound < max_id:
        upper_id_bound = min(lower_id_bound + BATCH_SIZE, max_id)
        with connection.cursor() as cursor:
            query = SQL("""
                INSERT INTO zerver_channelemailaddress (realm_id, channel_id, creator_id, sender_id, email_token, date_created, deactivated)
                SELECT realm_id, id, creator_id, %(mail_gateway_bot_id)s, email_token, date_created, deactivated
                FROM zerver_stream
                WHERE id > %(lower_id_bound)s AND id <= %(upper_id_bound)s;
                """)
            cursor.execute(
                query,
                {
                    "mail_gateway_bot_id": mail_gateway_bot_id,
                    "lower_id_bound": lower_id_bound,
                    "upper_id_bound": upper_id_bound,
                },
            )

        print(f"Processed {upper_id_bound} / {max_id}")
        lower_id_bound += BATCH_SIZE


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("zerver", "0628_remove_realm_invite_to_realm_policy"),
    ]

    operations = [
        migrations.CreateModel(
            name="ChannelEmailAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "email_token",
                    models.CharField(
                        db_index=True,
                        default=generate_email_token_for_stream,
                        max_length=32,
                        unique=True,
                    ),
                ),
                ("date_created", models.DateTimeField(default=django.utils.timezone.now)),
                ("deactivated", models.BooleanField(default=False)),
                (
                    "channel",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="zerver.stream"
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "realm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="zerver.realm"
                    ),
                ),
                (
                    "sender",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["realm", "channel"],
                        name="zerver_channelemailaddress_realm_id_channel_id_idx",
                    )
                ],
                "unique_together": {("channel", "creator", "sender")},
            },
        ),
        migrations.RunPython(
            backfill_channelemailaddress, reverse_code=migrations.RunPython.noop, elidable=True
        ),
        migrations.RemoveField(
            model_name="stream",
            name="email_token",
        ),
    ]
