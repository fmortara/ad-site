# Generated by Django 2.2.15 on 2023-08-14 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buy', '0007_auto_20230814_1003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='rel_message',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
