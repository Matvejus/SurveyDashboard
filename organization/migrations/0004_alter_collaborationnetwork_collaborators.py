# Generated by Django 4.1.7 on 2023-06-07 09:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0003_alter_orgprofile_org_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collaborationnetwork',
            name='collaborators',
            field=models.ManyToManyField(blank=True, null=True, related_name='collaborators', to=settings.AUTH_USER_MODEL),
        ),
    ]
