# Generated by Django 3.1.2 on 2020-10-29 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website_pages', '0003_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='ticket_price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='ticket_quantity',
            field=models.IntegerField(null=True),
        ),
    ]