# Generated by Django 4.1.7 on 2023-05-17 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
        ('Survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='org_profiles',
            field=models.ManyToManyField(blank=True, to='organization.orgprofile'),
        ),
    ]
