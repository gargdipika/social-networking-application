# Generated by Django 5.0.6 on 2024-06-02 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_timestamp_friendrequest_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]