# Generated by Django 4.1.7 on 2024-01-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='license',
            name='code',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
