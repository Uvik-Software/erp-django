# Generated by Django 2.1.1 on 2019-02-03 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190121_1150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='phone',
        ),
        migrations.AddField(
            model_name='user',
            name='additional_info',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='user',
            name='date_joined_company',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='hospital_days',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AddField(
            model_name='user',
            name='vacation_days',
            field=models.IntegerField(default=0),
        ),
    ]
