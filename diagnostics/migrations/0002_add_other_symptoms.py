from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diagnostics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='diagnosisrequest',
            name='other_symptoms',
            field=models.TextField(blank=True, default='', help_text='Additional free-text symptoms entered by the patient.'),
        ),
    ]
