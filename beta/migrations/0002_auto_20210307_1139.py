# Generated by Django 3.1.6 on 2021-03-07 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beta', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='occupation',
            field=models.CharField(choices=[('Student', 'Student'), ('Non student', 'Non student')], default='Student', max_length=255),
        ),
    ]
