from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['created_at']},
        ),
        migrations.CreateModel(
            name='DashboardProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('dashboard', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='memberships',
                    to='tracker.dashboard',
                )),
                ('project', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='memberships',
                    to='tracker.project',
                )),
            ],
            options={'ordering': ['added_at'], 'unique_together': {('dashboard', 'project')}},
        ),
        migrations.AddField(
            model_name='dashboard',
            name='projects',
            field=models.ManyToManyField(
                blank=True,
                related_name='dashboards',
                through='tracker.DashboardProject',
                to='tracker.project',
            ),
        ),
    ]
