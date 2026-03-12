from django.db import models


class Dashboard(models.Model):
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
    name = models.CharField(max_length=200, default='New Project')

    def __str__(self):
        return self.name


class Milestone(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('complete', 'Complete'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=300)
    date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    cat = models.CharField(max_length=100, blank=True)
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
            'status': self.status,
            'cat': self.cat,
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
            'id': f'e{self.pk}',
            'db_id': self.pk,
            'title': self.title,
            'date': self.date.isoformat() if self.date else '',
            'etype': self.etype,
            'people': self.people,
            'source': self.source,
            'sourceName': self.source_name,
            'desc': self.desc,
        }
