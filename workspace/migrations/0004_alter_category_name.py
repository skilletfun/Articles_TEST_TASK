# Generated by Django 4.1.6 on 2023-02-05 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0003_rename_category_article_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]