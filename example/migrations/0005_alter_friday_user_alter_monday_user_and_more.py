# Generated by Django 5.1.2 on 2025-02-09 21:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0004_monday_cont_friday_saturday_sunday_thursday_tuesday_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='friday',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='friday', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='monday',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='monday', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='saturday',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='saturday', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sunday',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sunday', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='thursday',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='thursday', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='tuesday',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tuesday', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='wednesday',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wednesday', to=settings.AUTH_USER_MODEL),
        ),
    ]
