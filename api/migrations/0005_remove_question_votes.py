# Generated by Django 2.2.1 on 2019-05-29 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20190524_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='votes',
        ),
    ]