# Generated by Django 5.0 on 2024-01-18 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_maintenancerequest_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenancerequest',
            name='message',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
