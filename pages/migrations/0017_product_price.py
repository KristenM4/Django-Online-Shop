# Generated by Django 4.1.7 on 2023-03-30 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0016_rename_price_product_msrp'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
