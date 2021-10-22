# Generated by Django 3.2.8 on 2021-10-22 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_stats', '0002_auto_20211022_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpiindex',
            name='area',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='kpi_stats.kpiarea', verbose_name='область КПЭ'),
            preserve_default=False,
        ),
    ]
