# Generated by Django 3.1 on 2020-08-24 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_auto_20200824_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='stock',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]