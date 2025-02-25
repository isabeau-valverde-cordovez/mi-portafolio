# Generated by Django 5.1.6 on 2025-02-23 20:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("due_date", models.DateField()),
                (
                    "priority",
                    models.CharField(
                        choices=[("L", "Baja"), ("M", "Media"), ("H", "Alta")],
                        default="M",
                        max_length=1,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("P", "Pendiente"),
                            ("C", "Completada"),
                            ("E", "En progreso"),
                        ],
                        default="P",
                        max_length=1,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
