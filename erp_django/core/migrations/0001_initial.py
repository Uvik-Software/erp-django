# Generated by Django 2.1.1 on 2018-09-26 12:55

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('MANAGER', 'manager'), ('DEVELOPER', 'developer'), ('CLIENT', 'client'), ('JUST_CREATED', 'just created')], default='JUST_CREATED', max_length=30)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('position', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=300)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=50)),
                ('identification_number', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=3)),
                ('bank_account_number', models.IntegerField()),
                ('beneficiary', models.CharField(max_length=50)),
                ('iban', models.CharField(max_length=50)),
                ('swift', models.CharField(max_length=50)),
                ('bank_address', models.TextField()),
                ('sign', models.ImageField(upload_to='static/signs/')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Company Currency',
                'verbose_name': 'Company Currency',
            },
        ),
        migrations.CreateModel(
            name='Cv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_drive_link', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('hourly_rate', models.IntegerField()),
                ('birthday_date', models.DateField()),
                ('monthly_salary', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DevelopersOnProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('hours', models.FloatField(null=True)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Developer')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DevSalary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.TextField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('expected_payout_date', models.DateField()),
                ('status', models.CharField(choices=[('SENT', 'sent'), ('WAITING_FOR_PAYMENT', 'waiting for payment'), ('PAID', 'paid')], max_length=50)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_name', models.CharField(max_length=50)),
                ('manager_surname', models.CharField(max_length=100)),
                ('manager_email', models.EmailField(max_length=254)),
                ('manager_position', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('company_name', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('project_type', models.CharField(choices=[('OUTSTAFF', 'outstaff'), ('FIX_PRICE_PROJECT', 'fix price project'), ('TIME_AND_MATERIAL', 'time & material')], max_length=50)),
                ('project_description', models.TextField()),
                ('currency', models.CharField(max_length=20)),
                ('basic_price', models.FloatField(null=True)),
                ('all_time_money_spent', models.IntegerField()),
                ('deadline', models.DateField(null=True)),
                ('project_started_date', models.DateField(null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Client')),
                ('general_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ManagerInfo')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SentNotifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('UNPAID_INVOICE', 'unpaid invoice'), ('BIRTHDAY', 'birthday'), ('DEADLINE', 'deadline')], max_length=50)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('quantity', models.FloatField()),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('comments', models.TextField(null=True)),
                ('approved', models.BooleanField(default=False)),
                ('developer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Developer')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BirthdayNotification',
            fields=[
                ('sentnotifications_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SentNotifications')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Developer')),
            ],
            bases=('core.sentnotifications',),
        ),
        migrations.CreateModel(
            name='DeadlineNotifications',
            fields=[
                ('sentnotifications_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SentNotifications')),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project')),
            ],
            bases=('core.sentnotifications',),
        ),
        migrations.CreateModel(
            name='InvoiceNotifications',
            fields=[
                ('sentnotifications_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SentNotifications')),
            ],
            bases=('core.sentnotifications',),
        ),
        migrations.AddField(
            model_name='invoice',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AddField(
            model_name='developersonproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AddField(
            model_name='cv',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Developer'),
        ),
        migrations.AddField(
            model_name='invoicenotifications',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Invoice'),
        ),
    ]
