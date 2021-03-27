# Generated by Django 3.1.6 on 2021-03-27 11:30

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, unique=True)),
                ('hashId', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('rent', models.IntegerField()),
                ('size', models.IntegerField()),
                ('buildDate', models.DateTimeField(auto_now_add=True)),
                ('livingNumber', models.IntegerField()),
                ('nearestStation', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReviewProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=234)),
                ('year', models.CharField(max_length=4)),
                ('charge_id', models.CharField(max_length=234)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consent', models.BooleanField(default=True, help_text='Are you happy for us to anonymously upload your review to our property review site? Your review will be anonymised')),
                ('livingConfirmation', models.BooleanField(default=True, help_text='Do you confirm that you live or lived at the property in question?')),
                ('firstName', models.CharField(max_length=255)),
                ('contactPermisssion', models.BooleanField(default=True, help_text='Do you want us to contact you when we upload your review?')),
                ('reviewDate', models.DateField(auto_now_add=True)),
                ('moveIn', models.DateField()),
                ('moveOut', models.DateField()),
                ('occupation', models.CharField(choices=[('Student', 'Student'), ('Non student', 'Non student')], default='Student', max_length=255)),
                ('bedroomNumber', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], default=3, help_text='How many bedrooms was the house? ')),
                ('overallRating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How would you rate the property out of 5? [conditon, responsiveness of landlord/property management company/value for money/neighbourhood]')),
                ('overallMaintainance', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='What was the condition of the property and how well was it maintained? ')),
                ('buildingQuality', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='What was the quality of the building [considering pests, rodents, cleanliness and any damp or mould]?')),
                ('furnishings', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='What was the quality of the furnishings? ')),
                ('water', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How would you rate the water, heating and insulation of the property?')),
                ('whiteGoods', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How would you rate the quality of the white goods (dishwasher, washing machine, electrical appliances)')),
                ('maintainanceComment', models.CharField(blank=True, help_text='Any other comment?', max_length=255, null=True)),
                ('overallLandlord', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How would you rate the landlord/property management company?')),
                ('responsiveness', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How responsive was the landlord/property management company to an issues that were raised? ')),
                ('repairQuality', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How would you rate the quality of any repairs to any issues raised?')),
                ('movingInExperiance', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How would you rate the moving in process and experience? [Moving in dates, state of property etc] ')),
                ('movingOutExperiance', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How would you rate the moving out process and experience? [Deposit, cleanling fees, fairness] ')),
                ('landlordComment', models.CharField(blank=True, help_text='Any other comment?', max_length=255, null=True)),
                ('rent', models.PositiveIntegerField(default=500, help_text='What was your monthly rent?')),
                ('valueForMoney', models.BooleanField(default=True, help_text='Was the property worth the money?')),
                ('areaSafety', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How safe did you feel in the area?')),
                ('areaEnjoyment', models.IntegerField(choices=[(1, 1), (2, 2), (3, 2), (4, 4), (5, 5)], default=3, help_text='How much did you enjoy living in the area? ')),
                ('areaEnjoymentReason', models.CharField(blank=True, help_text='why? [amenities, closeness to transport, noise]', max_length=255, null=True)),
                ('recomendation', models.BooleanField(default=True, help_text='Would you reccomend this property to others? ')),
                ('property', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='beta.property')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('send_daily_emails', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
    ]
