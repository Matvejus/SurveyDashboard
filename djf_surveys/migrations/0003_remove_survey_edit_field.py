# Generated by Django 4.1.7 on 2024-03-09 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djf_surveys', '0002_alter_question_edit_field_alter_survey_edit_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='edit_field',
        ),
    ]
