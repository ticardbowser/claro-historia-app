from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_project_settings_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Rename api_key → client_id (repurpose the column cleanly)
        migrations.RenameField(
            model_name='project',
            old_name='google_api_key',
            new_name='google_client_id',
        ),
        migrations.AlterField(
            model_name='project',
            name='google_client_id',
            field=models.CharField(blank=True, max_length=300),
        ),
        # Add client_secret
        migrations.AddField(
            model_name='project',
            name='google_client_secret',
            field=models.CharField(blank=True, max_length=300),
        ),
        # Add GoogleOAuthToken table
        migrations.CreateModel(
            name='GoogleOAuthToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField()),
                ('refresh_token', models.TextField(blank=True)),
                ('expires_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='google_tokens', to='tracker.project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='google_tokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={'unique_together': {('user', 'project')}},
        ),
    ]
