# Generated by Django 2.2.28 on 2023-04-15 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='releaseprogress',
            name='version',
        ),
        migrations.DeleteModel(
            name='ReleaseTodo',
        ),
        migrations.DeleteModel(
            name='ReleaseProgress',
        ),
    ]