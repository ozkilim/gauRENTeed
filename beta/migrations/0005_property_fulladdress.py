# Generated by Django 3.1.6 on 2021-03-29 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beta', '0004_auto_20210329_0636'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='fullAddress',
            field=models.CharField(default='', max_length=255, unique=True),
        ),
    ]
