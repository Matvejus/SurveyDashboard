# Generated by Django 4.1.7 on 2023-06-29 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djf_surveys', '0004_alter_dimension_id_alter_subdimension_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimension',
            name='id',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subdimension',
            name='id',
            field=models.CharField(max_length=40, primary_key=True, serialize=False),
        ),
    ]