# Generated by Django 4.1.7 on 2023-03-24 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_product_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]