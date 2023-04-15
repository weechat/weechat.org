# Generated by Django 2.2.28 on 2023-04-15 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Keydate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('version', models.TextField(max_length=32)),
                ('text', models.TextField()),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=256)),
                ('filename', models.CharField(max_length=256)),
                ('comment', models.TextField(blank=True)),
                ('priority', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsortype', models.IntegerField(choices=[(0, 'Individual'), (1, 'Association'), (2, 'Company')], default=0)),
                ('name', models.CharField(max_length=64)),
                ('date', models.DateField()),
                ('site', models.CharField(blank=True, max_length=512)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('number', models.IntegerField(default=1)),
                ('comment', models.CharField(blank=True, max_length=1024)),
            ],
        ),
    ]
