# Generated by Django 3.0.7 on 2020-06-18 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200619_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listener',
            name='type',
            field=models.CharField(choices=[('USER', 'User'), ('ROOM', 'Room'), ('GROUP', 'Group')], max_length=5),
        ),
    ]
