import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('abbreviation', models.CharField(max_length=255, verbose_name='abbreviation')),
            ],
            options={
                'verbose_name': 'institute',
                'verbose_name_plural': 'institutes',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('abbreviation', models.CharField(max_length=255, verbose_name='abbreviation')),
            ],
            options={
                'verbose_name': 'institution',
                'verbose_name_plural': 'institutions',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('abbreviation', models.CharField(max_length=255, verbose_name='abbreviation')),
                ('institute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', related_query_name='department', to='units.institute', verbose_name='institute')),
            ],
            options={
                'verbose_name': 'department',
                'verbose_name_plural': 'departments',
            },
        ),
        migrations.AddField(
            model_name='institute',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='institutes', related_query_name='institute', to='units.institution', verbose_name='institution'),
        ),
    ]
