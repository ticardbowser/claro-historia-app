from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='date_started',
            field=models.DateField(blank=True, null=True, help_text='Date work began (in-progress)'),
        ),
        migrations.AddField(
            model_name='milestone',
            name='date_completed',
            field=models.DateField(blank=True, null=True, help_text='Date marked complete'),
        ),
    ]
