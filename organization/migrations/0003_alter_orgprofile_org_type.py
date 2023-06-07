# Generated by Django 4.1.7 on 2023-06-07 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgprofile',
            name='org_type',
            field=models.CharField(choices=[('GVR_F', 'Government - Federal or state government jurisdiction/agency'), ('GVR_L', 'Government - Local agency (e.g. district, municipality, regional)'), ('NGO', 'NGO - National or International'), ('PRIV_MULTI', 'Private sector - Multinational Corporation'), ('PRIV_NATIONAL', 'Private sector - National Corporation'), ('SMALLHOLDER', 'Smallholder producer'), ('PRODUCER', 'Producer organization'), ('FARMERS_ASC', "Farmers' association"), ('LABOR_UNION', 'Labor union'), ('OTHER', 'Other civil society organization (e.g. Women Association, Youth Association)')], max_length=20),
        ),
    ]