# Generated by Django 5.0.9 on 2024-11-16 07:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zerver", "0626_set_default_value_for_can_invite_users_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="realm",
            name="can_invite_users_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="+",
                to="zerver.usergroup",
            ),
        ),
    ]
