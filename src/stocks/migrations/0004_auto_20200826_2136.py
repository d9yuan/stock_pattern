# Generated by Django 3.1 on 2020-08-26 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_auto_20200824_2144'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='price',
            name='details',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='stocks.detailpage'),
        ),
    ]
