# Claro Historia — Django

A project history tracker for milestones and events, converted from a static HTML app to a full Django project with a persistent SQLite database and REST API.

## Setup

### 1. Install dependencies

```bash
pip install django
```

### 2. Apply database migrations

```bash
python manage.py migrate
```

### 3. (Optional) Load sample data

Seeds the database with the milestones and events from the original HTML file:

```bash
python manage.py seed_data
```

### 4. (Optional) Create an admin user

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** to use the app.
Visit **http://127.0.0.1:8000/admin** to manage data via Django admin.

---

## Project structure

```
claro_historia/          ← Django project package
    settings.py
    urls.py
    wsgi.py

tracker/                 ← Main app
    models.py            ← Project, Milestone, Event models
    views.py             ← Page view + REST API endpoints
    urls.py              ← URL routing
    admin.py             ← Django admin registration
    templates/
        tracker/
            index.html   ← Full UI (converted from original HTML)
    migrations/
    management/
        commands/
            seed_data.py ← Optional sample data loader

manage.py
```

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| PATCH  | `/api/projects/<id>/rename/` | Rename project |
| GET    | `/api/projects/<id>/milestones/` | List milestones |
| POST   | `/api/projects/<id>/milestones/` | Create milestone |
| PUT    | `/api/projects/<id>/milestones/<id>/` | Update milestone |
| DELETE | `/api/projects/<id>/milestones/<id>/` | Delete milestone |
| PATCH  | `/api/projects/<id>/milestones/<id>/cycle/` | Cycle milestone status |
| GET    | `/api/projects/<id>/events/` | List events |
| POST   | `/api/projects/<id>/events/` | Create event |
| PUT    | `/api/projects/<id>/events/<id>/` | Update event |
| DELETE | `/api/projects/<id>/events/<id>/` | Delete event |
