# Generated by Django 4.1.2 on 2024-04-19 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(blank=True, max_length=250, verbose_name='ID платежа'),
        ),
    ]
