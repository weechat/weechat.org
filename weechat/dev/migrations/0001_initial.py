# Generated by Django 2.2.28 on 2023-04-15 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visible', models.BooleanField(default=True)),
                ('tracker', models.CharField(blank=True, max_length=64)),
                ('spec', models.CharField(blank=True, max_length=512)),
                ('status', models.IntegerField(default=0)),
                ('commits', models.CharField(blank=True, max_length=1024)),
                ('component', models.CharField(default='core', max_length=64)),
                ('description', models.CharField(max_length=512)),
                ('priority', models.IntegerField(default=0)),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='download.Release')),
            ],
            options={
                'ordering': ['-version__date', 'priority'],
            },
        ),
    ]
