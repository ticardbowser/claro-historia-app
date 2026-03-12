from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_dashboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='resolved',
            field=models.BooleanField(default=False),
        ),
    ]
