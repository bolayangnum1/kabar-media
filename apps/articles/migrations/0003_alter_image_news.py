# Generated by Django 3.2.9 on 2022-01-16 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_rename_article_image_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='news',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='articles.article', verbose_name='Новость'),
        ),
    ]
