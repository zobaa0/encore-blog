# Generated by Django 4.0.6 on 2022-08-01 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_tag_article_article_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-article_published']},
        ),
    ]
