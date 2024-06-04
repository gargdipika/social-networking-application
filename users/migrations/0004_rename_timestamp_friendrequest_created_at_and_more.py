# Generated by Django 5.0.6 on 2024-06-02 08:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_friendrequest'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='timestamp',
            new_name='created_at',
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_sent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='to_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend_requests_received', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='friendrequest',
            name='accepted',
        ),
    ]