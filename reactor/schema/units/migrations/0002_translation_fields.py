from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='abbreviation_en',
            field=models.CharField(max_length=255, null=True, verbose_name='abbreviation'),
        ),
        migrations.AddField(
            model_name='department',
            name='abbreviation_pl',
            field=models.CharField(max_length=255, null=True, verbose_name='abbreviation'),
        ),
        migrations.AddField(
            model_name='department',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='department',
            name='name_pl',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='institute',
            name='abbreviation_en',
            field=models.CharField(max_length=255, null=True, verbose_name='abbreviation'),
        ),
        migrations.AddField(
            model_name='institute',
            name='abbreviation_pl',
            field=models.CharField(max_length=255, null=True, verbose_name='abbreviation'),
        ),
        migrations.AddField(
            model_name='institute',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='institute',
            name='name_pl',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='institution',
            name='abbreviation_en',
            field=models.CharField(max_length=255, null=True, verbose_name='abbreviation'),
        ),
        migrations.AddField(
            model_name='institution',
            name='abbreviation_pl',
            field=models.CharField(max_length=255, null=True, verbose_name='abbreviation'),
        ),
        migrations.AddField(
            model_name='institution',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='institution',
            name='name_pl',
            field=models.CharField(max_length=255, null=True, verbose_name='name'),
        ),
    ]
