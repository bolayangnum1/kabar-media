# Generated by Django 3.2.9 on 2022-01-16 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='article',
            new_name='news',
        ),
    ]
