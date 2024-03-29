# Generated by Django 4.2.6 on 2024-01-06 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ms18', '0003_rename_author_product_employee_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee', models.CharField(max_length=100)),
                ('date_posted', models.DateField()),
                ('title', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(default=0)),
                ('content', models.TextField()),
            ],
        ),
    ]
