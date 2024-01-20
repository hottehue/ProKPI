# Generated by Django 5.0 on 2023-12-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bf',
            fields=[
                ('budgetfinish_id', models.AutoField(primary_key=True, serialize=False)),
                ('budget_is', models.IntegerField(blank=True, null=True)),
                ('create_at', models.DateTimeField(blank=True, db_column='create at', null=True)),
            ],
            options={
                'db_table': 'bf',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Bp',
            fields=[
                ('budgetplan_id', models.AutoField(primary_key=True, serialize=False)),
                ('budget', models.IntegerField(blank=True, null=True)),
                ('create_at', models.DateTimeField(blank=True, db_column='create at', null=True)),
            ],
            options={
                'db_table': 'bp',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Phase',
            fields=[
                ('phase_id', models.AutoField(primary_key=True, serialize=False)),
                ('phase_name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'phase',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'project',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TempLoad',
            fields=[
                ('temp_load_id', models.AutoField(primary_key=True, serialize=False)),
                ('phase_id', models.IntegerField(blank=True, choices=[(1, 'Ist-Analyse'), (2, 'Soll-Konzept'), (3, 'Architektur-Bereich'), (4, 'End- & Zwischen-Architekturen'), (5, 'Architektur-Fahrplan')], null=True)),
                ('task_name', models.CharField(blank=True, max_length=255, null=True)),
                ('startdate', models.DateField(blank=True, null=True)),
                ('enddate', models.DateField(blank=True, null=True)),
                ('budget', models.IntegerField(blank=True, null=True)),
                ('startdate_is', models.DateField(blank=True, null=True)),
                ('enddate_is', models.DateField(blank=True, null=True)),
                ('budget_is', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'temp_load',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tf',
            fields=[
                ('tfinish_id', models.AutoField(primary_key=True, serialize=False)),
                ('startdate_is', models.DateField(blank=True, null=True)),
                ('enddate_is', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tf',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tn',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tn',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tp',
            fields=[
                ('tplan_id', models.AutoField(primary_key=True, serialize=False)),
                ('startdate', models.DateField(blank=True, null=True)),
                ('enddate', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tp',
                'managed': False,
            },
        ),
    ]
