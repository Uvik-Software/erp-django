# Generated by Django 2.1.1 on 2018-11-02 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20181031_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='owner',
            name='user_create',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
