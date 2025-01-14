# Generated by Django 5.0.4 on 2024-08-16 10:55

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restau', '0004_category_alter_menu_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='reservation',
            unique_together={('table', 'date', 'time')},
        ),
        migrations.RemoveField(
            model_name='table',
            name='is_available',
        ),
        migrations.AddField(
            model_name='reservation',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='reservation',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='reservation',
            name='first_name',
            field=models.CharField(default='H', max_length=50),
        ),
        migrations.AddField(
            model_name='reservation',
            name='last_name',
            field=models.CharField(default='H', max_length=50),
        ),
        migrations.AddField(
            model_name='reservation',
            name='phone',
            field=models.CharField(default='06666666', max_length=15),
        ),
        migrations.AddField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='restau.table'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='time',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='number_of_people',
            field=models.IntegerField(default='1'),
        ),
        migrations.AlterField(
            model_name='table',
            name='number',
            field=models.IntegerField(unique=True),
        ),
        migrations.DeleteModel(
            name='TableReservation',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='customer_phone',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='reservation_date',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='special_requests',
        ),
    ]
