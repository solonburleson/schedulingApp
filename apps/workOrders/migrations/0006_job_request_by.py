# Generated by Django 2.1.7 on 2019-04-10 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workOrders', '0005_client_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='request_by',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
