# Generated by Django 2.1.1 on 2019-01-10 13:27

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
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
                ('type', models.CharField(choices=[('MANAGER', 'Manager'), ('DEVELOPER', 'Developer'), ('CLIENT', 'Client'), ('JUST_CREATED', 'Just created')], default='JUST_CREATED', max_length=30)),
                ('address', models.TextField(blank=True, default='')),
                ('position', models.CharField(blank=True, default='', max_length=128)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ActOfPerfJobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('number_of_act', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BankInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=20, null=True)),
                ('bank_account_number', models.CharField(max_length=50, null=True)),
                ('bank_address', models.TextField(null=True)),
                ('bank_code', models.CharField(max_length=20, null=True)),
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
            ],
            options={
                'verbose_name': 'Company Currency',
                'verbose_name_plural': 'Company Currency',
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
            name='DeadlineForGCal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='DevelopersOnProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(null=True)),
                ('hours', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DevSalary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField(default=12, validators=[django.core.validators.MaxValueValidator(31), django.core.validators.MinValueValidator(1)])),
                ('comment', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('expected_payout_date', models.DateField()),
                ('status', models.CharField(choices=[('SENT', 'sent'), ('WAITING_FOR_PAYMENT', 'waiting for payment'), ('PAID', 'paid')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20, null=True)),
                ('last_name', models.CharField(max_length=50, null=True)),
                ('father_name', models.CharField(max_length=20, null=True)),
                ('address', models.TextField(null=True)),
                ('tax_number', models.CharField(max_length=20, null=True)),
                ('num_contract_with_dev', models.CharField(max_length=20, null=True)),
                ('date_contract_with_dev', models.DateField(null=True)),
                ('sign', models.ImageField(null=True, upload_to='static/signs/')),
                ('bank_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.BankInfo')),
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
                ('all_time_money_spent', models.IntegerField(default=0)),
                ('deadline', models.DateField(null=True)),
                ('project_started_date', models.DateField(null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Owner')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectStartForGCal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=150)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Project')),
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
            name='Vacation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('comments', models.TextField(null=True)),
                ('approved', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Owner')),
            ],
        ),
        migrations.CreateModel(
            name='BirthdayNotification',
            fields=[
                ('sentnotifications_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SentNotifications')),
            ],
            bases=('core.sentnotifications',),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=300)),
                ('phone', models.CharField(max_length=50)),
                ('identification_number', models.CharField(default='', max_length=32)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Owner')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('core.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='DeadlineNotifications',
            fields=[
                ('sentnotifications_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SentNotifications')),
            ],
            bases=('core.sentnotifications',),
        ),
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('father_name', models.CharField(blank=True, default='', max_length=20)),
                ('tax_number', models.CharField(default='', max_length=20)),
                ('hourly_rate', models.IntegerField()),
                ('birthday_date', models.DateField()),
                ('monthly_salary', models.IntegerField()),
                ('sign', models.ImageField(null=True, upload_to='static/signs/')),
                ('bank_info', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.BankInfo')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Owner')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('core.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceNotifications',
            fields=[
                ('sentnotifications_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.SentNotifications')),
            ],
            bases=('core.sentnotifications',),
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('core.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Owner'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AddField(
            model_name='devsalary',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Owner'),
        ),
        migrations.AddField(
            model_name='developersonproject',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Owner'),
        ),
        migrations.AddField(
            model_name='developersonproject',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AddField(
            model_name='deadlineforgcal',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AddField(
            model_name='company',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Owner'),
        ),
        migrations.AddField(
            model_name='actofperfjobs',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Owner'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='vacation',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Developer'),
        ),
        migrations.AddField(
            model_name='project',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Client'),
        ),
        migrations.AddField(
            model_name='project',
            name='manager_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Manager'),
        ),
        migrations.AddField(
            model_name='invoicenotifications',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Invoice'),
        ),
        migrations.AddField(
            model_name='developersonproject',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Developer'),
        ),
        migrations.AddField(
            model_name='deadlinenotifications',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Project'),
        ),
        migrations.AddField(
            model_name='cv',
            name='developer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Developer'),
        ),
        migrations.AddField(
            model_name='birthdaynotification',
            name='event_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Developer'),
        ),
        migrations.AddField(
            model_name='actofperfjobs',
            name='developer_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Developer'),
        ),
    ]