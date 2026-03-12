import json
from collections import defaultdict
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Dashboard, DashboardProject, Project, Milestone, Event, GoogleOAuthToken



# ── Access helpers ────────────────────────────────────────────────────────────

def _accessible_projects(user):
    """All projects are visible to any authenticated user."""
    return Project.objects.all()


def _get_project_or_403(project_id, user):
    """Any authenticated user can access any project."""
    return get_object_or_404(Project, pk=project_id)


# ── Shared aggregation helper ─────────────────────────────────────────────────

def _build_project_cards(projects, today):
    """Given a queryset/list of projects, return aggregated card data."""
    cards = []
    totals = dict(milestones=0, complete=0, in_progress=0, pending=0,
                  events=0, risks=0, hires=0)
    all_monthly = defaultdict(int)
    global_cats = defaultdict(int)
    global_etypes = defaultdict(int)

    for project in projects:
        ms = list(project.milestones.all())
        evs = list(project.events.all())

        n_total = len(ms)
        n_complete = sum(1 for m in ms if m.status == 'complete')
        n_inprog = sum(1 for m in ms if m.status == 'in-progress')
        n_pending = sum(1 for m in ms if m.status == 'pending')
        pct = round((n_complete / n_total) * 100) if n_total else 0

        upcoming = sorted(
            [m for m in ms if m.date and m.status != 'complete'
             and today <= m.date <= today + timedelta(days=60)],
            key=lambda m: m.date
        )
        dated_events = sorted([e for e in evs if e.date], key=lambda e: e.date, reverse=True)
        latest_event = dated_events[0] if dated_events else None

        etype_counts = defaultdict(int)
        for e in evs:
            etype_counts[e.etype] += 1
            global_etypes[e.etype] += 1
        for m in ms:
            if m.cat:
                global_cats[m.cat.strip()] += 1
        for m in ms:
            if m.date:
                all_monthly[m.date.strftime('%Y-%m')] += 1
        for e in evs:
            if e.date:
                all_monthly[e.date.strftime('%Y-%m')] += 1

        n_risks = sum(1 for e in evs if e.etype == 'risk' and not e.resolved)
        totals['milestones'] += n_total
        totals['complete'] += n_complete
        totals['in_progress'] += n_inprog
        totals['pending'] += n_pending
        totals['events'] += len(evs)
        totals['risks'] += n_risks
        totals['hires'] += etype_counts.get('hire', 0)

        cards.append({
            'project': project,
            'n_total': n_total,
            'n_complete': n_complete,
            'n_inprog': n_inprog,
            'n_pending': n_pending,
            'n_events': len(evs),
            'pct': pct,
            'upcoming': upcoming[:3],
            'latest_event': latest_event,
            'n_risks': n_risks,
        })

    cards.sort(key=lambda p: (-p['n_inprog'], -p['pct']))

    months = []
    for i in range(11, -1, -1):
        d = today.replace(day=1) - timedelta(days=i * 28)
        key = d.strftime('%Y-%m')
        months.append({'label': d.strftime('%b %Y'), 'key': key, 'count': all_monthly.get(key, 0)})
    max_monthly = max((m['count'] for m in months), default=1)

    etype_labels = {'hire': 'New Hire', 'depart': 'Departure', 'reorg': 'Reorg',
                    'tech': 'Technology', 'risk': 'Risk', 'note': 'Note'}
    etype_colors = {'hire': '#5b8fd4', 'depart': '#c47a5a', 'reorg': '#9b6fc4',
                    'tech': '#4ab8c4', 'risk': '#c45050', 'note': '#8a8680'}
    event_type_breakdown = [
        {'key': k, 'label': etype_labels.get(k, k), 'count': v, 'color': etype_colors.get(k, '#888')}
        for k, v in sorted(global_etypes.items(), key=lambda x: -x[1])
    ]
    top_cats = sorted(global_cats.items(), key=lambda x: -x[1])[:8]
    global_pct = round((totals['complete'] / totals['milestones']) * 100) if totals['milestones'] else 0

    return cards, totals, months, max_monthly, event_type_breakdown, top_cats, global_pct


# ── Dashboards home ───────────────────────────────────────────────────────────

@login_required
def dashboards_home(request):
    dashboards = Dashboard.objects.prefetch_related('projects').filter(owner=request.user)
    all_projects = Project.objects.all()
    return render(request, 'tracker/dashboards_home.html', {
        'dashboards': dashboards,
        'all_projects': all_projects,
        'today': date.today(),
    })


# ── Single dashboard view ─────────────────────────────────────────────────────

@login_required
def dashboard(request, dashboard_id):
    db = get_object_or_404(
        Dashboard.objects.prefetch_related('projects__milestones', 'projects__events'),
        pk=dashboard_id, owner=request.user,
    )
    all_projects = Project.objects.all()
    dashboard_project_ids = set(db.projects.values_list('id', flat=True))
    today = date.today()

    projects = list(db.projects.prefetch_related('milestones', 'events').all())
    cards, totals, months, max_monthly, event_type_breakdown, top_cats, global_pct = \
        _build_project_cards(projects, today)

    return render(request, 'tracker/dashboard.html', {
        'dashboard': db,
        'all_projects': all_projects,
        'dashboard_project_ids': dashboard_project_ids,
        'project_cards': cards,
        'n_projects': len(cards),
        'total_milestones': totals['milestones'],
        'total_complete': totals['complete'],
        'total_in_progress': totals['in_progress'],
        'total_pending': totals['pending'],
        'total_events': totals['events'],
        'total_risks': totals['risks'],
        'total_hires': totals['hires'],
        'global_pct': global_pct,
        'months': months,
        'max_monthly': max_monthly,
        'event_type_breakdown': event_type_breakdown,
        'top_cats': top_cats,
        'today': today,
    })


# ── Dashboard CRUD ────────────────────────────────────────────────────────────

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def dashboard_create(request):
    data = json.loads(request.body)
    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
    project_ids = data.get('project_ids', [])
    db = Dashboard.objects.create(name=name, owner=request.user)
    for pid in project_ids:
        try:
            p = Project.objects.get(pk=pid)
            DashboardProject.objects.create(dashboard=db, project=p)
        except Project.DoesNotExist:
            pass
    return JsonResponse({'id': db.pk, 'name': db.name}, status=201)


@login_required
@csrf_exempt
@require_http_methods(['PATCH'])
def dashboard_rename(request, dashboard_id):
    db = get_object_or_404(Dashboard, pk=dashboard_id, owner=request.user)
    data = json.loads(request.body)
    db.name = data.get('name', db.name).strip() or db.name
    db.save()
    return JsonResponse({'id': db.pk, 'name': db.name})


@login_required
@csrf_exempt
@require_http_methods(['DELETE'])
def dashboard_delete(request, dashboard_id):
    db = get_object_or_404(Dashboard, pk=dashboard_id, owner=request.user)
    db.delete()
    return JsonResponse({'deleted': True})


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def dashboard_add_project(request, dashboard_id):
    db = get_object_or_404(Dashboard, pk=dashboard_id, owner=request.user)
    data = json.loads(request.body)
    project = get_object_or_404(Project, pk=data.get('project_id'))
    DashboardProject.objects.get_or_create(dashboard=db, project=project)
    return JsonResponse({'dashboard_id': db.pk, 'project_id': project.pk, 'project_name': project.name})


@login_required
@csrf_exempt
@require_http_methods(['DELETE'])
def dashboard_remove_project(request, dashboard_id, project_id):
    db = get_object_or_404(Dashboard, pk=dashboard_id, owner=request.user)
    DashboardProject.objects.filter(dashboard=db, project_id=project_id).delete()
    return JsonResponse({'deleted': True})


# ── Project CRUD ──────────────────────────────────────────────────────────────

@login_required
@csrf_exempt
@require_http_methods(['POST'])
def project_create(request):
    data = json.loads(request.body)
    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
    project = Project.objects.create(name=name, owner=request.user)
    return JsonResponse({'id': project.pk, 'name': project.name}, status=201)


@login_required
@csrf_exempt
@require_http_methods(['PATCH'])
def project_rename(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    data = json.loads(request.body)
    project.name = data.get('name', project.name).strip() or project.name
    project.save()
    return JsonResponse({'id': project.pk, 'name': project.name})


@login_required
@csrf_exempt
@require_http_methods(['DELETE'])
def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return JsonResponse({'deleted': True})


# ── Project tracker page ──────────────────────────────────────────────────────

@login_required
def index(request, project_id):
    project = _get_project_or_403(project_id, request.user)
    milestones = [m.to_dict() for m in project.milestones.all()]
    events = [e.to_dict() for e in project.events.all()]
    return render(request, 'tracker/index.html', {
        'project': project,
        'milestones_json': json.dumps(milestones),
        'events_json': json.dumps(events),
    })


# ── Milestones ────────────────────────────────────────────────────────────────

@login_required
@csrf_exempt
@require_http_methods(['GET', 'POST'])
def milestone_list(request, project_id):
    project = _get_project_or_403(project_id, request.user)
    if request.method == 'GET':
        return JsonResponse([m.to_dict() for m in project.milestones.all()], safe=False)
    data = json.loads(request.body)
    m = Milestone.objects.create(
        project=project,
        title=data['title'],
        date=data.get('date') or None,
        date_started=data.get('dateStarted') or None,
        date_completed=data.get('dateCompleted') or None,
        status=data.get('status', 'pending'),
        cat=data.get('cat', ''),
        owner=data.get('owner', ''),
        source=data.get('source', ''),
        source_name=data.get('sourceName', ''),
        desc=data.get('desc', ''),
    )
    return JsonResponse(m.to_dict(), status=201)


@login_required
@csrf_exempt
@require_http_methods(['PUT', 'DELETE'])
def milestone_detail(request, project_id, milestone_id):
    m = get_object_or_404(Milestone, pk=milestone_id, project_id=project_id, project__in=_accessible_projects(request.user))
    if request.method == 'DELETE':
        m.delete()
        return JsonResponse({'deleted': True})
    data = json.loads(request.body)
    m.title = data.get('title', m.title)
    m.date = data.get('date') or None
    m.date_started = data.get('dateStarted') or None
    m.date_completed = data.get('dateCompleted') or None
    m.status = data.get('status', m.status)
    m.cat = data.get('cat', m.cat)
    m.owner = data.get('owner', m.owner)
    m.source = data.get('source', m.source)
    m.source_name = data.get('sourceName', m.source_name)
    m.desc = data.get('desc', m.desc)
    m.save()
    return JsonResponse(m.to_dict())


@login_required
@csrf_exempt
@require_http_methods(['PATCH'])
def milestone_cycle(request, project_id, milestone_id):
    m = get_object_or_404(Milestone, pk=milestone_id, project_id=project_id, project__in=_accessible_projects(request.user))
    order = ['pending', 'in-progress', 'complete']
    m.status = order[(order.index(m.status) + 1) % len(order)]
    m.save()
    return JsonResponse(m.to_dict())


# ── Events ────────────────────────────────────────────────────────────────────

@login_required
@csrf_exempt
@require_http_methods(['GET', 'POST'])
def event_list(request, project_id):
    project = _get_project_or_403(project_id, request.user)
    if request.method == 'GET':
        return JsonResponse([e.to_dict() for e in project.events.all()], safe=False)
    data = json.loads(request.body)
    e = Event.objects.create(
        project=project,
        title=data['title'],
        date=data.get('date') or None,
        etype=data.get('etype', 'note'),
        people=data.get('people', ''),
        owner=data.get('owner', ''),
        source=data.get('source', ''),
        source_name=data.get('sourceName', ''),
        desc=data.get('desc', ''),
    )
    return JsonResponse(e.to_dict(), status=201)


@login_required
@csrf_exempt
@require_http_methods(['PUT', 'DELETE'])
def event_detail(request, project_id, event_id):
    e = get_object_or_404(Event, pk=event_id, project_id=project_id, project__in=_accessible_projects(request.user))
    if request.method == 'DELETE':
        e.delete()
        return JsonResponse({'deleted': True})
    data = json.loads(request.body)
    e.title = data.get('title', e.title)
    e.date = data.get('date') or None
    e.etype = data.get('etype', e.etype)
    e.people = data.get('people', e.people)
    e.owner = data.get('owner', e.owner)
    e.source = data.get('source', e.source)
    e.source_name = data.get('sourceName', e.source_name)
    e.desc = data.get('desc', e.desc)
    e.save()
    return JsonResponse(e.to_dict())


@login_required
@csrf_exempt
@require_http_methods(['PATCH'])
def event_resolve(request, project_id, event_id):
    e = get_object_or_404(Event, pk=event_id, project_id=project_id, project__in=_accessible_projects(request.user))
    data = json.loads(request.body)
    e.resolved = data.get('resolved', not e.resolved)
    e.save()
    return JsonResponse(e.to_dict())


# ── Cross-project analysis view ───────────────────────────────────────────────

@login_required
def analysis(request):
    all_projects = Project.objects.prefetch_related('milestones', 'events').order_by('name')

    # Parse selected project IDs from query string: ?p=1&p=3&p=7
    selected_ids = request.GET.getlist('p')
    try:
        selected_ids = [int(i) for i in selected_ids if i]
    except ValueError:
        selected_ids = []

    selected_projects = []
    project_data = []

    if selected_ids:
        selected_projects = list(Project.objects.filter(pk__in=selected_ids))
        # Preserve selection order
        selected_projects.sort(key=lambda p: selected_ids.index(p.pk))

        # Palette for up to 8 projects — distinct, readable on dark bg
        PALETTE = [
            '#e8a246', '#4ab8c4', '#9b6fc4', '#5b8fd4',
            '#4a9e7a', '#c47a5a', '#c4b44a', '#c45090',
        ]

        today = date.today()

        for idx, project in enumerate(selected_projects):
            ms = list(project.milestones.order_by('date'))
            evs = list(project.events.order_by('date'))
            color = PALETTE[idx % len(PALETTE)]

            n_total    = len(ms)
            n_complete = sum(1 for m in ms if m.status == 'complete')
            n_inprog   = sum(1 for m in ms if m.status == 'in-progress')
            n_pending  = sum(1 for m in ms if m.status == 'pending')
            pct        = round((n_complete / n_total) * 100) if n_total else 0

            # Category breakdown
            cats = defaultdict(int)
            for m in ms:
                if m.cat:
                    cats[m.cat.strip()] += 1

            # Event type breakdown
            etypes = defaultdict(int)
            for e in evs:
                etypes[e.etype] += 1

            # Owner activity (milestones + events)
            owners = defaultdict(int)
            for m in ms:
                if m.owner:
                    owners[m.owner.strip()] += 1
            for e in evs:
                if e.owner:
                    owners[e.owner.strip()] += 1

            # Open risks
            open_risks = [e for e in evs if e.etype == 'risk' and not e.resolved]
            resolved_risks = [e for e in evs if e.etype == 'risk' and e.resolved]

            # Date span
            dated_ms = [m for m in ms if m.date]
            span_start = min(m.date for m in dated_ms).isoformat() if dated_ms else None
            span_end   = max(m.date for m in dated_ms).isoformat() if dated_ms else None

            # Upcoming milestones (next 90 days)
            upcoming = [m for m in ms if m.date and m.status != 'complete' and today <= m.date <= today + timedelta(days=90)]

            # Monthly activity (milestones + events combined, last 24 months)
            monthly = defaultdict(int)
            for m in ms:
                if m.date:
                    monthly[m.date.strftime('%Y-%m')] += 1
            for e in evs:
                if e.date:
                    monthly[e.date.strftime('%Y-%m')] += 1

            project_data.append({
                'project': project,
                'color': color,
                'idx': idx,
                'n_total': n_total,
                'n_complete': n_complete,
                'n_inprog': n_inprog,
                'n_pending': n_pending,
                'n_events': len(evs),
                'pct': pct,
                'cats': sorted(cats.items(), key=lambda x: -x[1])[:10],
                'etypes': dict(etypes),
                'owners': sorted(owners.items(), key=lambda x: -x[1])[:8],
                'open_risks': open_risks,
                'resolved_risks': resolved_risks,
                'n_risks_open': len(open_risks),
                'n_risks_resolved': len(resolved_risks),
                'span_start': span_start,
                'span_end': span_end,
                'upcoming': upcoming[:5],
                'monthly_json': json.dumps(dict(monthly)),
                'etypes_json': json.dumps(dict(etypes)),
                'cats_json': json.dumps(sorted(cats.items(), key=lambda x: -x[1])[:10]),
                'owners_json': json.dumps(sorted(owners.items(), key=lambda x: -x[1])[:8]),
                'milestones_json': json.dumps([m.to_dict() for m in ms]),
                'events_json': json.dumps([e.to_dict() for e in evs]),
            })

        # Build shared 24-month axis
        months_axis = []
        for i in range(23, -1, -1):
            d = today.replace(day=1) - timedelta(days=i * 30)
            months_axis.append({'key': d.strftime('%Y-%m'), 'label': d.strftime("%b '%y")})

    return render(request, 'tracker/analysis.html', {
        'all_projects': all_projects,
        'selected_ids': selected_ids,
        'project_data': project_data,
        'months_axis': json.dumps([m['key'] for m in (months_axis if selected_ids else [])]),
        'months_labels': json.dumps([m['label'] for m in (months_axis if selected_ids else [])]),
        'has_selection': bool(selected_ids),
    })

# ── Auth views ────────────────────────────────────────────────────────────────

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboards_home')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'dashboards_home'))
        error = 'Invalid username or password.'
    return render(request, 'tracker/login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboards_home')
    error = None
    if request.method == 'POST':
        username   = request.POST.get('username', '').strip()
        password   = request.POST.get('password', '')
        password2  = request.POST.get('password2', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        if not username or not password:
            error = 'Username and password are required.'
        elif password != password2:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            error = 'That username is already taken.'
        else:
            user = User.objects.create_user(
                username=username, password=password,
                first_name=first_name, last_name=last_name,
            )
            login(request, user)
            return redirect('dashboards_home')
    return render(request, 'tracker/register.html', {'error': error})

# ── Project settings page ─────────────────────────────────────────────────────

@login_required
def project_settings(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    dashboards_featuring = project.dashboards.filter(owner=request.user)
    all_user_dashboards = Dashboard.objects.filter(owner=request.user)
    oauth_connected = GoogleOAuthToken.objects.filter(
        user=request.user, project=project
    ).exists()
    oauth_error = request.GET.get('oauth_error', '')
    oauth_ok    = request.GET.get('oauth_ok', '')
    return render(request, 'tracker/project_settings.html', {
        'project': project,
        'dashboards_featuring': dashboards_featuring,
        'all_user_dashboards': all_user_dashboards,
        'milestone_count': project.milestones.count(),
        'event_count': project.events.count(),
        'oauth_connected': oauth_connected,
        'oauth_error': oauth_error,
        'oauth_ok': oauth_ok,
    })


@login_required
@csrf_exempt
@require_http_methods(['POST', 'PATCH'])
def project_settings_save(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    project.name                     = data.get('name', project.name).strip() or project.name
    project.description              = data.get('description', project.description)
    project.google_client_id         = data.get('google_client_id', project.google_client_id).strip()
    project.google_client_secret     = data.get('google_client_secret', project.google_client_secret).strip()
    project.google_drive_folder_id   = data.get('google_drive_folder_id', project.google_drive_folder_id).strip()
    project.google_drive_folder_name = data.get('google_drive_folder_name', project.google_drive_folder_name).strip()
    project.save()
    return JsonResponse({
        'id': project.pk,
        'name': project.name,
        'description': project.description,
        'google_client_id': project.google_client_id,
        'google_client_secret': project.google_client_secret,
        'google_drive_folder_id': project.google_drive_folder_id,
        'google_drive_folder_name': project.google_drive_folder_name,
    })

# ── Google Drive / OAuth ──────────────────────────────────────────────────────

import requests as _requests
from urllib.parse import urlencode
from django.utils import timezone
from datetime import timedelta
from .models import GoogleOAuthToken

DRIVE_FILES_URL    = 'https://www.googleapis.com/drive/v3/files'
GOOGLE_AUTH_URL    = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL   = 'https://oauth2.googleapis.com/token'
GOOGLE_REVOKE_URL  = 'https://oauth2.googleapis.com/revoke'
DRIVE_SCOPE        = 'https://www.googleapis.com/auth/drive.readonly'

DRIVE_MIME_ICONS = {
    'application/vnd.google-apps.document':     ('📄', 'Doc'),
    'application/vnd.google-apps.spreadsheet':  ('📊', 'Sheet'),
    'application/vnd.google-apps.presentation': ('📑', 'Slides'),
    'application/vnd.google-apps.folder':       ('📁', 'Folder'),
    'application/pdf':                          ('📕', 'PDF'),
    'image/png':                                ('🖼', 'Image'),
    'image/jpeg':                               ('🖼', 'Image'),
    'text/plain':                               ('📝', 'Text'),
    'application/zip':                          ('🗜', 'ZIP'),
}


def _get_redirect_uri(request, project_id):
    return request.build_absolute_uri(f'/api/projects/{project_id}/drive/oauth/callback/')


def _refresh_token(token_obj, client_id, client_secret):
    """Refresh an expired access token. Updates token_obj in place and saves."""
    if not token_obj.refresh_token:
        return False
    resp = _requests.post(GOOGLE_TOKEN_URL, data={
        'client_id':     client_id,
        'client_secret': client_secret,
        'refresh_token': token_obj.refresh_token,
        'grant_type':    'refresh_token',
    }, timeout=10)
    if not resp.ok:
        return False
    data = resp.json()
    token_obj.access_token = data['access_token']
    token_obj.expires_at = timezone.now() + timedelta(seconds=data.get('expires_in', 3600))
    token_obj.save()
    return True


@login_required
def drive_oauth_start(request, project_id):
    """Redirect user to Google's OAuth consent screen."""
    project = get_object_or_404(Project, pk=project_id)
    if not project.google_client_id or not project.google_client_secret:
        return redirect(f'/project/{project_id}/settings/#integrations')

    params = {
        'client_id':     project.google_client_id,
        'redirect_uri':  _get_redirect_uri(request, project_id),
        'response_type': 'code',
        'scope':         DRIVE_SCOPE,
        'access_type':   'offline',
        'prompt':        'consent',   # force refresh_token every time
        'state':         str(project_id),
    }
    return redirect(f'{GOOGLE_AUTH_URL}?{urlencode(params)}')


@login_required
def drive_oauth_callback(request, project_id):
    """Handle Google's redirect back after user consent."""
    project = get_object_or_404(Project, pk=project_id)
    error = request.GET.get('error')
    if error:
        return redirect(f'/project/{project_id}/settings/?oauth_error={error}#integrations')

    code = request.GET.get('code')
    if not code:
        return redirect(f'/project/{project_id}/settings/?oauth_error=no_code#integrations')

    # Exchange code for tokens
    resp = _requests.post(GOOGLE_TOKEN_URL, data={
        'code':          code,
        'client_id':     project.google_client_id,
        'client_secret': project.google_client_secret,
        'redirect_uri':  _get_redirect_uri(request, project_id),
        'grant_type':    'authorization_code',
    }, timeout=10)

    if not resp.ok:
        return redirect(f'/project/{project_id}/settings/?oauth_error=token_exchange_failed#integrations')

    data = resp.json()
    expires_at = timezone.now() + timedelta(seconds=data.get('expires_in', 3600))

    GoogleOAuthToken.objects.update_or_create(
        user=request.user,
        project=project,
        defaults={
            'access_token':  data['access_token'],
            'refresh_token': data.get('refresh_token', ''),
            'expires_at':    expires_at,
        }
    )
    return redirect(f'/project/{project_id}/settings/?oauth_ok=1#drive-files')


@login_required
@csrf_exempt
@require_http_methods(['POST'])
def drive_oauth_disconnect(request, project_id):
    """Revoke and delete the stored token for this user+project."""
    project = get_object_or_404(Project, pk=project_id)
    try:
        token_obj = GoogleOAuthToken.objects.get(user=request.user, project=project)
        # Best-effort revoke with Google
        try:
            _requests.post(GOOGLE_REVOKE_URL,
                           params={'token': token_obj.access_token}, timeout=5)
        except Exception:
            pass
        token_obj.delete()
    except GoogleOAuthToken.DoesNotExist:
        pass
    return JsonResponse({'disconnected': True})


@login_required
@csrf_exempt
@require_http_methods(['GET'])
def drive_files(request, project_id):
    """List files in the project's linked Google Drive folder."""
    project = get_object_or_404(Project, pk=project_id)

    if not project.google_client_id or not project.google_client_secret:
        return JsonResponse({'error': 'no_credentials',
                             'message': 'OAuth credentials not configured for this project.'}, status=400)
    if not project.google_drive_folder_id:
        return JsonResponse({'error': 'no_folder',
                             'message': 'No Drive folder linked to this project.'}, status=400)

    try:
        token_obj = GoogleOAuthToken.objects.get(user=request.user, project=project)
    except GoogleOAuthToken.DoesNotExist:
        return JsonResponse({'error': 'not_connected',
                             'message': 'Google Drive not connected. Click Connect in Project Settings.'}, status=401)

    # Refresh if expired
    if token_obj.is_expired():
        if not _refresh_token(token_obj, project.google_client_id, project.google_client_secret):
            token_obj.delete()
            return JsonResponse({'error': 'token_expired',
                                 'message': 'Session expired. Please reconnect Google Drive in Project Settings.'}, status=401)

    page_token = request.GET.get('pageToken', '')
    folder_id  = request.GET.get('folderId', '') or project.google_drive_folder_id

    headers = {'Authorization': f'Bearer {token_obj.access_token}'}
    params = {
        'q':        f"'{folder_id}' in parents and trashed = false",
        'fields':   'nextPageToken,files(id,name,mimeType,modifiedTime,size,webViewLink,owners)',
        'orderBy':  'modifiedTime desc',
        'pageSize': 50,
    }
    if page_token:
        params['pageToken'] = page_token

    try:
        resp = _requests.get(DRIVE_FILES_URL, headers=headers, params=params, timeout=10)
        data = resp.json()
    except Exception as e:
        return JsonResponse({'error': 'request_failed', 'message': str(e)}, status=502)

    if resp.status_code == 401:
        # Token rejected — clear it so user reconnects
        token_obj.delete()
        return JsonResponse({'error': 'token_invalid',
                             'message': 'Access token rejected. Please reconnect Google Drive.'}, status=401)
    if not resp.ok:
        msg = data.get('error', {}).get('message', f'Drive API error {resp.status_code}')
        return JsonResponse({'error': 'api_error', 'message': msg}, status=resp.status_code)

    files = data.get('files', [])
    for f in files:
        icon, label = DRIVE_MIME_ICONS.get(f.get('mimeType', ''), ('📄', 'File'))
        f['_icon']      = icon
        f['_typeLabel'] = label

    return JsonResponse({
        'files':         files,
        'nextPageToken': data.get('nextPageToken', ''),
        'folder_name':   project.google_drive_folder_name or project.google_drive_folder_id,
    })

