# Generated by Django 4.1.7 on 2023-03-28 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_remove_order_hidden_orderitem_hidden'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='hidden',
        ),
    ]
