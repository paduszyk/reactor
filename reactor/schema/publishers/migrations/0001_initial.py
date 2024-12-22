import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('evaluation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublishingHouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('abbreviation', models.CharField(blank=True, max_length=255, verbose_name='abbreviation')),
            ],
            options={
                'verbose_name': 'publishing house',
                'verbose_name_plural': 'publishing houses',
            },
        ),
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('abbreviation', models.CharField(max_length=255, verbose_name='abbreviation')),
                ('issn_p', models.CharField(blank=True, max_length=255, verbose_name='p-ISSN')),
                ('issn_e', models.CharField(blank=True, max_length=255, verbose_name='e-ISSN')),
                ('disciplines', models.ManyToManyField(blank=True, related_name='journals', related_query_name='journal', to='evaluation.discipline', verbose_name='disciplines')),
                ('publishing_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journals', related_query_name='journal', to='publishers.publishinghouse', verbose_name='publishing house')),
            ],
            options={
                'verbose_name': 'journal',
                'verbose_name_plural': 'journals',
            },
        ),
    ]
