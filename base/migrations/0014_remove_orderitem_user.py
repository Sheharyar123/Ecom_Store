# Generated by Django 4.1.1 on 2022-09-15 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_rename_customer_orderitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
    ]