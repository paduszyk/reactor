import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('evaluation', '0001_initial'),
        ('hr', '0001_initial'),
        ('publishers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='title')),
                ('file', models.FileField(blank=True, upload_to='', verbose_name='file')),
                ('application_number', models.CharField(max_length=255, verbose_name='application number')),
                ('date_applied', models.DateField(verbose_name='date applied')),
                ('patent_number', models.CharField(blank=True, max_length=255, verbose_name='patent number')),
                ('date_granted', models.DateField(blank=True, null=True, verbose_name='date granted')),
                ('implemented', models.BooleanField(default=False, verbose_name='implemented')),
            ],
            options={
                'verbose_name': 'patent',
                'verbose_name_plural': 'patents',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='title')),
                ('year_published', models.PositiveSmallIntegerField(verbose_name='year published')),
                ('doi', models.CharField(blank=True, max_length=255, verbose_name='DOI')),
                ('file', models.FileField(blank=True, upload_to='', verbose_name='file')),
                ('volume', models.CharField(blank=True, max_length=255, verbose_name='volume')),
                ('issue', models.CharField(blank=True, max_length=255, verbose_name='issue')),
                ('pagination', models.CharField(blank=True, max_length=255, verbose_name='pagination')),
                ('journal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', related_query_name='article', to='publishers.journal', verbose_name='journal')),
            ],
            options={
                'verbose_name': 'article',
                'verbose_name_plural': 'articles',
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alias', models.CharField(blank=True, max_length=255, verbose_name='alias')),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='authors', related_query_name='author', to='hr.contract', verbose_name='contract')),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='title')),
                ('year_published', models.PositiveSmallIntegerField(verbose_name='year published')),
                ('doi', models.CharField(blank=True, max_length=255, verbose_name='DOI')),
                ('file', models.FileField(blank=True, upload_to='', verbose_name='file')),
                ('edited', models.BooleanField(default=False, verbose_name='edited')),
                ('isbn', models.CharField(blank=True, max_length=255, verbose_name='ISBN')),
                ('publishing_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', related_query_name='book', to='publishers.publishinghouse', verbose_name='publishing house')),
            ],
            options={
                'verbose_name': 'book',
                'verbose_name_plural': 'books',
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(verbose_name='title')),
                ('doi', models.CharField(blank=True, max_length=255, verbose_name='DOI')),
                ('file', models.FileField(blank=True, upload_to='', verbose_name='file')),
                ('pagination', models.CharField(blank=True, max_length=255, verbose_name='pagination')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', related_query_name='chapter', to='output.book', verbose_name='book')),
            ],
            options={
                'verbose_name': 'chapter',
                'verbose_name_plural': 'chapters',
            },
        ),
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField(verbose_name='order')),
                ('work_id', models.PositiveBigIntegerField(verbose_name='work ID')),
                ('unit_id', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='unit ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='output.author', verbose_name='author')),
                ('discipline', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contributions', related_query_name='contribution', to='evaluation.discipline', verbose_name='discipline')),
                ('unit_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='contenttypes.contenttype', verbose_name='unit type')),
                ('work_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='contenttypes.contenttype', verbose_name='work type')),
            ],
            options={
                'verbose_name': 'contribution',
                'verbose_name_plural': 'contributions',
            },
        ),
    ]
