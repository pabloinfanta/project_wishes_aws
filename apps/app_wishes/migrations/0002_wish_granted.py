# Generated by Django 2.2.4 on 2021-10-02 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_wishes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='granted',
            field=models.BooleanField(default=False),
        ),
    ]
