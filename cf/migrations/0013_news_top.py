# Generated by Django 3.0 on 2020-03-27 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cf', '0012_auto_20200110_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='top',
            field=models.BooleanField(default=False),
        ),
    ]
