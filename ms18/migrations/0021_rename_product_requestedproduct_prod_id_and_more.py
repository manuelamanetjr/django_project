# Generated by Django 5.0.1 on 2024-01-14 12:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ms18', '0020_requisition_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requestedproduct',
            old_name='product',
            new_name='PROD_ID',
        ),
        migrations.RenameField(
            model_name='requestedproduct',
            old_name='REQ_PROD_ID',
            new_name='REQUESTED_PRODUCT_ID',
        ),
        migrations.RenameField(
            model_name='requestedproduct',
            old_name='REQ_PROD_NAME',
            new_name='REQUESTED_PRODUCT_NAME',
        ),
        migrations.RenameField(
            model_name='requisition',
            old_name='status',
            new_name='REQ_STATUS',
        ),
        migrations.RemoveField(
            model_name='requestedproduct',
            name='REQ_PROD_DATE_ADDED',
        ),
        migrations.RemoveField(
            model_name='requestedproduct',
            name='REQ_PROD_QUANTITY',
        ),
        migrations.RemoveField(
            model_name='requisition',
            name='REQ_DESCRIPTION',
        ),
        migrations.RemoveField(
            model_name='requisition',
            name='REQ_NAME',
        ),
        migrations.RemoveField(
            model_name='requisition',
            name='REQ_QUANTITY',
        ),
        migrations.RemoveField(
            model_name='requisition',
            name='requested_product',
        ),
        migrations.AddField(
            model_name='requestedproduct',
            name='REQUESTED_PRODUCT_QUANTITY',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='requisition',
            name='REQUESTED_PRODUCT_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ms18.requestedproduct'),
        ),
        migrations.AddField(
            model_name='requisition',
            name='REQ_DATE_CREATEDAT',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='requisition',
            name='SUPPLIER_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ms18.supplier'),
        ),
    ]