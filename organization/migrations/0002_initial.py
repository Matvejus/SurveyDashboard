# Generated by Django 4.1.7 on 2024-01-05 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collaborationnetwork',
            name='collaborators',
            field=models.ManyToManyField(related_name='collaborators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collaborationnetwork',
            name='license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.license'),
        ),
        migrations.AddField(
            model_name='collaborationnetwork',
            name='orchestrator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='orchestrator', to=settings.AUTH_USER_MODEL),
        ),
    ]
