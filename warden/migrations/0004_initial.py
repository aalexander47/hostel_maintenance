# Generated by Django 5.0 on 2024-01-07 19:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('warden', '0003_delete_customuser'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Warden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('Hostel_name', models.CharField(choices=[('SOE Wing Hostel (D Block)', 'SOE Wing Hostel (D Block)'), ('SOE Wing Hostel ( E Block)', 'SOE Wing Hostel ( E Block)'), ('SOE Wing Hostel (F Block)', 'SOE Wing Hostel (F Block)'), ('Institute of Design ', 'Institute of Design '), ('SOE Wing Hostel (D  Block)', 'SOE Wing Hostel (D  Block)'), ('New Staff Quarters  No 1', 'New Staff Quarters  No 1'), ('New Staff Quarters  No 2', 'New Staff Quarters  No 2'), ('Boat Club', 'Boat Club'), ('Raj', 'Raj'), ('Sangeet Kala Academy', 'Sangeet Kala Academy'), ('Gurukul C Block', 'Gurukul C Block'), ('Institute of Design  No 1', 'Institute of Design  No 1'), ('Institute of Design  No 2', 'Institute of Design  No 2'), ('Anuja 1', 'Anuja 1'), ('Anuja 2', 'Anuja 2'), ('Anuja 3', 'Anuja 3'), ('Anuja 4', 'Anuja 4'), ('Nalini Pride', 'Nalini Pride'), ('Vitthal Krupa', 'Vitthal Krupa'), ('Anuja 5', 'Anuja 5'), ('Anuja 6', 'Anuja 6'), ('Shakuntala', 'Shakuntala'), ('Shree Aangan', 'Shree Aangan'), ('Vaishnavi Pride', 'Vaishnavi Pride'), ('Vaishnavi Complex', 'Vaishnavi Complex')], max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
