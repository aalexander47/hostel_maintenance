# Generated by Django 5.0 on 2024-01-08 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0003_alter_maintenancerequest_technician'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='enrollment_no',
            field=models.CharField(max_length=255, null=True),
        ),
    ]