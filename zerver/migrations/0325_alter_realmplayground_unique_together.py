# Generated by Django 3.2.2 on 2021-05-13 00:16

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("zerver", "0324_fix_deletion_cascade_behavior"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="realmplayground",
            unique_together={("realm", "pygments_language", "name")},
        ),
    ]
