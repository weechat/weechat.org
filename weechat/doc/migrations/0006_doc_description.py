# Generated by Django 2.2.28 on 2023-05-19 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doc', '0005_doc_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='doc',
            name='description',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='doc',
            name='url',
            field=models.CharField(blank=True, max_length=512),
        ),
    ]
