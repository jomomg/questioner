# Generated by Django 2.2.1 on 2019-05-24 08:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190524_0753'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='topic',
            new_name='title',
        ),
    ]
