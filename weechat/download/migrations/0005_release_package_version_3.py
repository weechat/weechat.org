# Generated by Django 2.2.28 on 2023-04-15 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('download', '0004_release_package_version_2'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='package',
            options={'ordering': ['version', '-type__priority']},
        ),
        migrations.RemoveField(
            model_name='package',
            name='version_string',
        ),
    ]