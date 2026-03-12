from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_event_resolved'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='owner',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
