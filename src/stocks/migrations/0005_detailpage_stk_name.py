# Generated by Django 3.1 on 2020-08-26 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_auto_20200826_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailpage',
            name='stk_name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
