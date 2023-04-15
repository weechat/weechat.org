# Generated by Django 2.2.28 on 2023-04-15 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Release',
            fields=[
                ('version', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('description', models.CharField(blank=True, max_length=64)),
                ('date', models.DateField(blank=True, null=True)),
                ('security_issues_fixed', models.IntegerField(default=0)),
                ('securityfix', models.CharField(blank=True, max_length=256)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ReleaseTodo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1024)),
                ('priority', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('type', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('priority', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=256)),
                ('icon', models.CharField(blank=True, max_length=64)),
                ('directory', models.CharField(blank=True, max_length=256)),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='ReleaseProgress',
            fields=[
                ('version', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='download.Release')),
                ('done', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'release progress',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, max_length=512)),
                ('sha1sum', models.CharField(blank=True, max_length=128)),
                ('sha512sum', models.CharField(blank=True, max_length=128)),
                ('display_time', models.BooleanField(default=False)),
                ('directory', models.CharField(blank=True, max_length=256)),
                ('url', models.CharField(blank=True, max_length=512)),
                ('text', models.CharField(blank=True, max_length=512)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='download.Type')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='download.Release')),
            ],
            options={
                'ordering': ['version', '-type__priority'],
            },
        ),
    ]
