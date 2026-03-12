from django.db import models
from django.contrib.auth.models import User


class Dashboard(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboards_owned', null=True)
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    projects = models.ManyToManyField(
        'Project',
        through='DashboardProject',
        related_name='dashboards',
        blank=True,
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class DashboardProject(models.Model):
    """Explicit through-table so we can control ordering."""
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE, related_name='memberships')
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='memberships')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('dashboard', 'project')
        ordering = ['added_at']


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_owned', null=True)
    name = models.CharField(max_length=200, default='New Project')
    description = models.TextField(blank=True)
    google_client_id = models.CharField(max_length=300, blank=True)
    google_client_secret = models.CharField(max_length=300, blank=True)
    google_drive_folder_id = models.CharField(max_length=200, blank=True)
    google_drive_folder_name = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class GoogleOAuthToken(models.Model):
    """Per-user, per-project OAuth tokens for Google Drive access."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='google_tokens')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='google_tokens')
    access_token = models.TextField()
    refresh_token = models.TextField(blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f'{self.user.username} / {self.project.name}'

    def is_expired(self):
        from django.utils import timezone
        if not self.expires_at:
            return False
        return timezone.now() >= self.expires_at - timedelta(seconds=60)


from datetime import timedelta


class Milestone(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('complete', 'Complete'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=300)
    date = models.DateField(null=True, blank=True, help_text='Target / due date')
    date_started = models.DateField(null=True, blank=True, help_text='Date work began (in-progress)')
    date_completed = models.DateField(null=True, blank=True, help_text='Date marked complete')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cat = models.CharField(max_length=100, blank=True)
    owner = models.CharField(max_length=200, blank=True)
    source = models.URLField(blank=True)
    source_name = models.CharField(max_length=200, blank=True)
    desc = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.pk,
            'title': self.title,
            'date': self.date.isoformat() if self.date else '',
            'dateStarted': self.date_started.isoformat() if self.date_started else '',
            'dateCompleted': self.date_completed.isoformat() if self.date_completed else '',
            'status': self.status,
            'cat': self.cat,
            'owner': self.owner,
            'source': self.source,
            'sourceName': self.source_name,
            'desc': self.desc,
        }


class Event(models.Model):
    TYPE_CHOICES = [
        ('hire', 'New Hire'),
        ('depart', 'Departure'),
        ('reorg', 'Reorganization'),
        ('tech', 'Technology'),
        ('risk', 'Risk / Blocker'),
        ('note', 'General Note'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=300)
    date = models.DateField(null=True, blank=True)
    etype = models.CharField(max_length=20, choices=TYPE_CHOICES, default='note')
    people = models.CharField(max_length=300, blank=True)
    owner = models.CharField(max_length=200, blank=True)
    source = models.URLField(blank=True)
    source_name = models.CharField(max_length=200, blank=True)
    desc = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': f'e{self.pk}',
            'db_id': self.pk,
            'title': self.title,
            'date': self.date.isoformat() if self.date else '',
            'etype': self.etype,
            'people': self.people,
            'owner': self.owner,
            'source': self.source,
            'sourceName': self.source_name,
            'desc': self.desc,
            'resolved': self.resolved,
        }
