# Generated by Django 2.1.1 on 2019-01-11 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='owner',
            name='bank_info',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.BankInfo'),
        ),
    ]