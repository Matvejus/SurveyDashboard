# Generated by Django 4.1.7 on 2023-06-09 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djf_surveys', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='org_profiles',
        ),
        migrations.AddField(
            model_name='survey',
            name='org_type',
            field=models.CharField(default=1, max_length=20, verbose_name='Organization type'),
            preserve_default=False,
        ),
    ]
