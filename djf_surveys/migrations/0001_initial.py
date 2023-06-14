# Generated by Django 4.1.7 on 2023-06-14 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.TextField(help_text='The value of the answer given by the user.', verbose_name='value')),
            ],
            options={
                'verbose_name': 'answer',
                'verbose_name_plural': 'answers',
                'ordering': ['question__ordering'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('level', models.CharField(choices=[('Indv', 'Individual'), ('Org', 'Organizational'), ('NET', 'Network')], max_length=20)),
                ('dimension', models.CharField(choices=[('Solutions', 'Co-creating solutions'), ('Activities', 'Facilitating activities'), ('Partnerships', 'Brokering partnerships'), ('Legitimacy', 'Establishing legitimacy'), ('Solutions', 'Co-creating solutions'), ('Activities', 'Facilitating activities'), ('Partnerships', 'Brokering partnerships'), ('Legitimacy', 'Establishing legitimacy'), ('Solutions', 'Co-creating solutions'), ('Activities', 'Facilitating activities'), ('Partnerships', 'Brokering partnerships')], max_length=20)),
                ('key', models.CharField(blank=True, help_text='Unique key for this question, fill in the blank if you want to use for automatic generation.', max_length=225, null=True, unique=True, verbose_name='key')),
                ('label', models.CharField(help_text='Enter your question in here.', max_length=500, verbose_name='label')),
                ('type_field', models.PositiveSmallIntegerField(choices=[(0, 'Text'), (1, 'Number'), (2, 'Radio'), (3, 'Select'), (4, 'Multi Select'), (5, 'Text Area'), (6, 'URL'), (7, 'Email'), (8, 'Date'), (9, 'Rating')], verbose_name='type of input field')),
                ('choices', models.TextField(blank=True, help_text='If type of field is radio, select, or multi select, fill in the options separated by commas. Ex: Male, Female.', null=True, verbose_name='choices')),
                ('help_text', models.CharField(blank=True, help_text='You can add a help text in here.', max_length=200, null=True, verbose_name='help text')),
                ('required', models.BooleanField(default=True, help_text='If True, the user must provide an answer to this question.', verbose_name='required')),
                ('ordering', models.PositiveIntegerField(default=0, help_text='Defines the question order within the surveys.', verbose_name='choices')),
            ],
            options={
                'verbose_name': 'question',
                'verbose_name_plural': 'questions',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(default='', verbose_name='description')),
                ('slug', models.SlugField(default='', max_length=225, verbose_name='slug')),
                ('editable', models.BooleanField(default=True, help_text="If False, user can't edit record.", verbose_name='editable')),
                ('deletable', models.BooleanField(default=True, help_text="If False, user can't delete record.", verbose_name='deletable')),
                ('duplicate_entry', models.BooleanField(default=False, help_text='If True, user can resubmit.', verbose_name='mutiple submissions')),
                ('private_response', models.BooleanField(default=False, help_text='If True, only admin and owner can access.', verbose_name='private response')),
                ('can_anonymous_user', models.BooleanField(default=False, help_text='If True, user without authentatication can submit.', verbose_name='anonymous submission')),
            ],
            options={
                'verbose_name': 'survey',
                'verbose_name_plural': 'surveys',
            },
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djf_surveys.survey', verbose_name='survey')),
            ],
            options={
                'verbose_name': 'user answer',
                'verbose_name_plural': 'user answers',
                'ordering': ['-updated_at'],
            },
        ),
    ]
