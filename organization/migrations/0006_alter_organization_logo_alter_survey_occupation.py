# Generated by Django 4.1.7 on 2023-03-09 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_survey_organization_alter_survey_occupation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='logo',
            field=models.ImageField(blank=True, upload_to='uploads'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='occupation',
            field=models.CharField(choices=[('STUD', 'Student'), ('EMP', 'Employee')], max_length=10),
        ),
    ]
