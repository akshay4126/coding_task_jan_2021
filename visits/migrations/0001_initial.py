# Generated by Django 3.1.5 on 2021-01-10 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('level', models.IntegerField()),
                ('gcode', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_count', models.IntegerField(default=0)),
                ('visit_label', models.CharField(default='UNKNOWN', max_length=128)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='visits.location')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='visits.person')),
            ],
        ),
    ]