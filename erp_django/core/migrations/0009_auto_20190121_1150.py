# Generated by Django 2.1.1 on 2019-01-21 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190121_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developersonproject',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Owner'),
        ),
    ]
