# Generated by Django 2.1.1 on 2019-01-18 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20190116_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('MANAGER', 'Manager'), ('DEVELOPER', 'Developer'), ('CLIENT', 'Client'), ('JUST_CREATED', 'Just created'), ('ADMIN', 'Admin')], default='JUST_CREATED', max_length=30),
        ),
    ]
