# Generated by Django 4.1.7 on 2023-03-26 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_order_hidden'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='hidden',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
