# Generated by Django 5.0.1 on 2024-01-12 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ms18', '0014_rename_prod_id_requestedproduct_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestedproduct',
            name='user',
        ),
        migrations.AddField(
            model_name='requestedproduct',
            name='REQ_PROD_NAME',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
