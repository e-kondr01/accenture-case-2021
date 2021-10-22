# Generated by Django 3.2.8 on 2021-10-22 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_stats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpiindex',
            name='is_target_value_more',
            field=models.BooleanField(default=True, verbose_name='целевое значение должно быть больше?'),
        ),
        migrations.AlterField(
            model_name='kpientry',
            name='value',
            field=models.PositiveSmallIntegerField(verbose_name='значение (в процентах)'),
        ),
        migrations.AlterField(
            model_name='kpiindex',
            name='target_value',
            field=models.PositiveSmallIntegerField(verbose_name='целевое значние (в процентах)'),
        ),
    ]