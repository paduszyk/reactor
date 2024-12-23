import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('publishers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImpactFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value_2_year', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='2-year value')),
                ('value_5_year', models.DecimalField(decimal_places=3, max_digits=6, verbose_name='5-year value')),
                ('year_published', models.PositiveSmallIntegerField(verbose_name='year published')),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='impact_factors', related_query_name='impact_factor', to='publishers.journal', verbose_name='journal')),
            ],
            options={
                'verbose_name': 'Impact Factor',
                'verbose_name_plural': 'Impact Factors',
            },
        ),
        migrations.CreateModel(
            name='MinistryScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(verbose_name='value')),
                ('date_published', models.DateField(verbose_name='date published')),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ministry_scores', related_query_name='ministry_score', to='publishers.journal', verbose_name='journal')),
            ],
            options={
                'verbose_name': 'ministry score',
                'verbose_name_plural': 'ministry scores',
            },
        ),
    ]
