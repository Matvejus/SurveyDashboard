# Generated by Django 4.1.7 on 2023-12-04 19:15

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CollaborationNetwork',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=160)),
                ('stage', models.CharField(choices=[('START', 'Starting phase of the collaboration'), ('MIDDLE', 'Middle stage'), ('END', 'Final stage of the collaboration')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Full name', models.CharField(max_length=100)),
                ('Company', models.CharField(max_length=100)),
                ('Role', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='OrgProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('org_type', models.CharField(choices=[('GVR_F', 'Government - Federal or state government'), ('GVR_L', 'Government - Local agency'), ('NGO', 'NGO - National or International'), ('PRIV_MULTI', 'Private sector - Multinational Corporation'), ('PRIV_NATIONAL', 'Private sector - National Corporation'), ('SMALLHOLDER', 'Smallholder producer'), ('PRODUCER', 'Producer organization'), ('FARMERS_ASC', "Farmers' association"), ('LABOR_UNION', 'Labor union'), ('OTHER', 'Other civil society organization')], max_length=250)),
                ('vision', models.CharField(blank=True, max_length=250)),
                ('num_employees', models.CharField(max_length=20)),
                ('founded', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(2023)])),
                ('email', models.EmailField(max_length=255)),
            ],
        ),
    ]
