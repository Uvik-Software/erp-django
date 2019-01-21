# Generated by Django 2.1.1 on 2019-01-21 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20190118_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Owner'),
        ),
        migrations.AlterField(
            model_name='developer',
            name='bank_info',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.BankInfo'),
        ),
        migrations.AlterField(
            model_name='developer',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Owner'),
        ),
        migrations.AlterField(
            model_name='developer',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Client'),
        ),
        migrations.AlterField(
            model_name='project',
            name='manager_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Manager'),
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Owner'),
        ),
    ]
