# Generated by Django 3.1 on 2021-05-26 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocp_app', '0004_forum'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]