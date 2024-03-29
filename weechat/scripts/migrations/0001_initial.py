# Generated by Django 2.2.28 on 2023-04-15 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Script',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(default=False)),
                ('popularity', models.IntegerField()),
                ('name', models.CharField(max_length=32)),
                ('version', models.CharField(max_length=32)),
                ('url', models.CharField(blank=True, max_length=512)),
                ('language', models.CharField(max_length=32)),
                ('license', models.CharField(max_length=32)),
                ('md5sum', models.CharField(blank=True, max_length=32)),
                ('sha512sum', models.CharField(blank=True, max_length=128)),
                ('tags', models.CharField(blank=True, max_length=512)),
                ('desc_en', models.CharField(max_length=1024)),
                ('approval', models.CharField(blank=True, max_length=1024)),
                ('disabled', models.CharField(blank=True, max_length=1024)),
                ('requirements', models.CharField(blank=True, max_length=512)),
                ('min_weechat', models.CharField(blank=True, max_length=32)),
                ('max_weechat', models.CharField(blank=True, max_length=32)),
                ('author', models.CharField(max_length=256)),
                ('mail', models.EmailField(max_length=256)),
                ('added', models.DateTimeField()),
                ('updated', models.DateTimeField(null=True)),
            ],
            options={
                'ordering': ['-added'],
            },
        ),
    ]
