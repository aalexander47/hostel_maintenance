# Generated by Django 5.0 on 2023-12-27 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_maintenancerequest_completion_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenancerequest',
            name='completion_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]