import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('evaluation', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'position',
                'verbose_name_plural': 'positions',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
            ],
            options={
                'verbose_name': 'status',
                'verbose_name_plural': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255, verbose_name='last name')),
                ('given_names', models.CharField(max_length=255, verbose_name='given names')),
                ('degree', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='persons', related_query_name='person', to='evaluation.degree', verbose_name='degree')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='person', related_query_name='person', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
            },
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_id', models.PositiveBigIntegerField(verbose_name='unit ID')),
                ('disciplines', models.ManyToManyField(blank=True, related_name='contracts', related_query_name='contract', to='evaluation.discipline', verbose_name='disciplines')),
                ('unit_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='contenttypes.contenttype', verbose_name='unit type')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', related_query_name='contract', to='hr.person', verbose_name='person')),
                ('position', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contracts', related_query_name='contract', to='hr.position', verbose_name='position')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', related_query_name='contract', to='hr.status', verbose_name='status')),
            ],
            options={
                'verbose_name': 'contract',
                'verbose_name_plural': 'contracts',
            },
        ),
        migrations.CreateModel(
            name='Subgroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subgroups', related_query_name='subgroup', to='hr.group', verbose_name='group')),
            ],
            options={
                'verbose_name': 'subgroup',
                'verbose_name_plural': 'subgroups',
            },
        ),
        migrations.AddField(
            model_name='position',
            name='subgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='positions', related_query_name='position', to='hr.subgroup', verbose_name='subgroup'),
        ),
    ]
