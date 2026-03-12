import json
from collections import defaultdict
from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from .models import Dashboard, DashboardProject, Project, Milestone, Event


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

        n_risks = etype_counts.get('risk', 0)
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

def dashboards_home(request):
    dashboards = Dashboard.objects.prefetch_related('projects').all()
    all_projects = Project.objects.all()
    return render(request, 'tracker/dashboards_home.html', {
        'dashboards': dashboards,
        'all_projects': all_projects,
        'today': date.today(),
    })


# ── Single dashboard view ─────────────────────────────────────────────────────

def dashboard(request, dashboard_id):
    db = get_object_or_404(
        Dashboard.objects.prefetch_related('projects__milestones', 'projects__events'),
        pk=dashboard_id,
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

@csrf_exempt
@require_http_methods(['POST'])
def dashboard_create(request):
    data = json.loads(request.body)
    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
    project_ids = data.get('project_ids', [])
    db = Dashboard.objects.create(name=name)
    for pid in project_ids:
        try:
            p = Project.objects.get(pk=pid)
            DashboardProject.objects.create(dashboard=db, project=p)
        except Project.DoesNotExist:
            pass
    return JsonResponse({'id': db.pk, 'name': db.name}, status=201)


@csrf_exempt
@require_http_methods(['PATCH'])
def dashboard_rename(request, dashboard_id):
    db = get_object_or_404(Dashboard, pk=dashboard_id)
    data = json.loads(request.body)
    db.name = data.get('name', db.name).strip() or db.name
    db.save()
    return JsonResponse({'id': db.pk, 'name': db.name})


@csrf_exempt
@require_http_methods(['DELETE'])
def dashboard_delete(request, dashboard_id):
    db = get_object_or_404(Dashboard, pk=dashboard_id)
    db.delete()
    return JsonResponse({'deleted': True})


@csrf_exempt
@require_http_methods(['POST'])
def dashboard_add_project(request, dashboard_id):
    db = get_object_or_404(Dashboard, pk=dashboard_id)
    data = json.loads(request.body)
    project = get_object_or_404(Project, pk=data.get('project_id'))
    DashboardProject.objects.get_or_create(dashboard=db, project=project)
    return JsonResponse({'dashboard_id': db.pk, 'project_id': project.pk, 'project_name': project.name})


@csrf_exempt
@require_http_methods(['DELETE'])
def dashboard_remove_project(request, dashboard_id, project_id):
    db = get_object_or_404(Dashboard, pk=dashboard_id)
    DashboardProject.objects.filter(dashboard=db, project_id=project_id).delete()
    return JsonResponse({'deleted': True})


# ── Project CRUD ──────────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(['POST'])
def project_create(request):
    data = json.loads(request.body)
    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)
    project = Project.objects.create(name=name)
    return JsonResponse({'id': project.pk, 'name': project.name}, status=201)


@csrf_exempt
@require_http_methods(['PATCH'])
def project_rename(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    data = json.loads(request.body)
    project.name = data.get('name', project.name).strip() or project.name
    project.save()
    return JsonResponse({'id': project.pk, 'name': project.name})


@csrf_exempt
@require_http_methods(['DELETE'])
def project_delete(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    project.delete()
    return JsonResponse({'deleted': True})


# ── Project tracker page ──────────────────────────────────────────────────────

def index(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    milestones = [m.to_dict() for m in project.milestones.all()]
    events = [e.to_dict() for e in project.events.all()]
    return render(request, 'tracker/index.html', {
        'project': project,
        'milestones_json': json.dumps(milestones),
        'events_json': json.dumps(events),
    })


# ── Milestones ────────────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def milestone_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'GET':
        return JsonResponse([m.to_dict() for m in project.milestones.all()], safe=False)
    data = json.loads(request.body)
    m = Milestone.objects.create(
        project=project,
        title=data['title'],
        date=data.get('date') or None,
        status=data.get('status', 'pending'),
        cat=data.get('cat', ''),
        source=data.get('source', ''),
        source_name=data.get('sourceName', ''),
        desc=data.get('desc', ''),
    )
    return JsonResponse(m.to_dict(), status=201)


@csrf_exempt
@require_http_methods(['PUT', 'DELETE'])
def milestone_detail(request, project_id, milestone_id):
    m = get_object_or_404(Milestone, pk=milestone_id, project_id=project_id)
    if request.method == 'DELETE':
        m.delete()
        return JsonResponse({'deleted': True})
    data = json.loads(request.body)
    m.title = data.get('title', m.title)
    m.date = data.get('date') or None
    m.status = data.get('status', m.status)
    m.cat = data.get('cat', m.cat)
    m.source = data.get('source', m.source)
    m.source_name = data.get('sourceName', m.source_name)
    m.desc = data.get('desc', m.desc)
    m.save()
    return JsonResponse(m.to_dict())


@csrf_exempt
@require_http_methods(['PATCH'])
def milestone_cycle(request, project_id, milestone_id):
    m = get_object_or_404(Milestone, pk=milestone_id, project_id=project_id)
    order = ['pending', 'in-progress', 'complete']
    m.status = order[(order.index(m.status) + 1) % len(order)]
    m.save()
    return JsonResponse(m.to_dict())


# ── Events ────────────────────────────────────────────────────────────────────

@csrf_exempt
@require_http_methods(['GET', 'POST'])
def event_list(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'GET':
        return JsonResponse([e.to_dict() for e in project.events.all()], safe=False)
    data = json.loads(request.body)
    e = Event.objects.create(
        project=project,
        title=data['title'],
        date=data.get('date') or None,
        etype=data.get('etype', 'note'),
        people=data.get('people', ''),
        source=data.get('source', ''),
        source_name=data.get('sourceName', ''),
        desc=data.get('desc', ''),
    )
    return JsonResponse(e.to_dict(), status=201)


@csrf_exempt
@require_http_methods(['PUT', 'DELETE'])
def event_detail(request, project_id, event_id):
    e = get_object_or_404(Event, pk=event_id, project_id=project_id)
    if request.method == 'DELETE':
        e.delete()
        return JsonResponse({'deleted': True})
    data = json.loads(request.body)
    e.title = data.get('title', e.title)
    e.date = data.get('date') or None
    e.etype = data.get('etype', e.etype)
    e.people = data.get('people', e.people)
    e.source = data.get('source', e.source)
    e.source_name = data.get('sourceName', e.source_name)
    e.desc = data.get('desc', e.desc)
    e.save()
    return JsonResponse(e.to_dict())
