# Generated by Django 2.2.4 on 2021-10-02 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_wishes', '0003_auto_20211002_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish',
            name='granted',
        ),
        migrations.DeleteModel(
            name='Granted',
        ),
    ]