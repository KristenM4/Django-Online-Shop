# Generated by Django 4.1.7 on 2023-03-30 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_remove_orderitem_hidden'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=2),
        ),
    ]
