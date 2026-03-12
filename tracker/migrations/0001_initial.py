from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Website Redesign', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(
                    choices=[('pending', 'Pending'), ('in-progress', 'In Progress'), ('complete', 'Complete')],
                    default='pending', max_length=20)),
                ('cat', models.CharField(blank=True, max_length=100)),
                ('source', models.URLField(blank=True)),
                ('source_name', models.CharField(blank=True, max_length=200)),
                ('desc', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                    related_name='milestones', to='tracker.project')),
            ],
            options={'ordering': ['date']},
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('date', models.DateField(blank=True, null=True)),
                ('etype', models.CharField(
                    choices=[('hire', 'New Hire'), ('depart', 'Departure'), ('reorg', 'Reorganization'),
                             ('tech', 'Technology'), ('risk', 'Risk / Blocker'), ('note', 'General Note')],
                    default='note', max_length=20)),
                ('people', models.CharField(blank=True, max_length=300)),
                ('source', models.URLField(blank=True)),
                ('source_name', models.CharField(blank=True, max_length=200)),
                ('desc', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                    related_name='events', to='tracker.project')),
            ],
            options={'ordering': ['date']},
        ),
    ]
