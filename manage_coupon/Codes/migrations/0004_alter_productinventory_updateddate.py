# Generated by Django 4.0 on 2021-12-17 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Codes', '0003_alter_product_updateddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinventory',
            name='updatedDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
