# Claro Historia

A Django application for tracking project history — milestones, events, people, risks, and decisions — across an organisation. Built around a dark, typographic UI with multi-user access, dashboard-based views, and optional Google Drive integration.

---

## Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Data Model](#data-model)
- [User Accounts & Access Control](#user-accounts--access-control)
- [Pages & Features](#pages--features)
  - [Dashboards Home](#dashboards-home)
  - [Dashboard View](#dashboard-view)
  - [Project Tracker](#project-tracker)
  - [Project Settings](#project-settings)
  - [Cross-Project Analysis](#cross-project-analysis)
- [API Reference](#api-reference)
- [Google Drive Integration](#google-drive-integration)
- [Seed Data](#seed-data)
- [Configuration](#configuration)
- [Migrations](#migrations)

---

## Quick Start

```bash
# Install dependencies (Django + requests)
pip install django requests

# Apply all migrations
python manage.py migrate

# (Optional) Load sample org data
python manage.py seed_org

# Run the development server
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser. You will be redirected to the login page.

**Sample accounts** (created by `seed_org`, all passwords: `password`):

| Username | Name | Role |
|---|---|---|
| `jordan.ellis` | Jordan Ellis | IC — 4 projects, 1 dashboard |
| `marcus.webb` | Marcus Webb | Manager — 5 projects, 1 dashboard |
| `rachel.torres` | Rachel Torres | Director — 10 projects, 1 dashboard |

---

## Architecture

```
claro_historia/          Django project package
    settings.py
    urls.py

tracker/                 Main application
    models.py            Dashboard, Project, Milestone, Event, GoogleOAuthToken
    views.py             All page views and API endpoints
    urls.py              URL routing
    admin.py
    templates/tracker/
        login.html
        register.html
        dashboards_home.html
        dashboard.html
        index.html           Project tracker
        project_settings.html
        analysis.html
    management/commands/
        seed_data.py
        seed_multi.py
        seed_org.py          60-person org, 10 projects, 3 users
    migrations/
        0001_initial.py
        0002_dashboard.py
        0003_event_resolved.py
        0004_owner.py
        0005_milestone_dates.py
        0006_user_ownership.py
        0007_project_settings_fields.py
        0008_oauth.py
```

**Stack:** Django (SQLite), no external JS frameworks, no Django REST Framework. All API endpoints return JSON and are called by vanilla JS in the templates.

---

## Data Model

### Dashboard
Owned by a user. A named collection of projects. Multiple dashboards can include the same project. Deleting a dashboard does not delete its projects.

| Field | Type | Notes |
|---|---|---|
| `owner` | FK → User | The user who created and manages this dashboard |
| `name` | CharField | Display name |
| `created_at` | DateTimeField | Auto-set on creation |
| `projects` | M2M → Project | Via `DashboardProject` through-table |

### Project
Visible to all authenticated users. The `owner` field records who created it but does not restrict access.

| Field | Type | Notes |
|---|---|---|
| `owner` | FK → User | Creator (audit trail only) |
| `name` | CharField | |
| `description` | TextField | Optional free-text description |
| `google_client_id` | CharField | OAuth 2.0 Client ID for Drive integration |
| `google_client_secret` | CharField | OAuth 2.0 Client Secret |
| `google_drive_folder_id` | CharField | Drive folder to browse |
| `google_drive_folder_name` | CharField | Display label for the folder |
| `created_at` | DateTimeField | |

### Milestone
A dated deliverable or checkpoint within a project.

| Field | Type | Notes |
|---|---|---|
| `project` | FK → Project | |
| `title` | CharField | |
| `date` | DateField | Target / due date |
| `date_started` | DateField | When work began |
| `date_completed` | DateField | When marked complete |
| `status` | CharField | `pending`, `in-progress`, `complete` |
| `cat` | CharField | Category tag (free text) |
| `owner` | CharField | Accountable person (name, not FK) |
| `source` | URLField | Reference URL |
| `source_name` | CharField | Display name for the source link |
| `desc` | TextField | Notes / description |

### Event
A moment in project history — a hire, departure, reorg, technology decision, risk, or general note.

| Field | Type | Notes |
|---|---|---|
| `project` | FK → Project | |
| `title` | CharField | |
| `date` | DateField | |
| `etype` | CharField | `hire`, `depart`, `reorg`, `tech`, `risk`, `note` |
| `people` | CharField | People involved (free text) |
| `owner` | CharField | Accountable person |
| `source` | URLField | |
| `source_name` | CharField | |
| `desc` | TextField | |
| `resolved` | BooleanField | Used for risk tracking — resolved risks are struck through |

### GoogleOAuthToken
Stores per-user, per-project OAuth tokens for Google Drive access. One token per (user, project) pair.

| Field | Type | Notes |
|---|---|---|
| `user` | FK → User | |
| `project` | FK → Project | |
| `access_token` | TextField | Current Bearer token |
| `refresh_token` | TextField | Used to refresh expired access tokens |
| `expires_at` | DateTimeField | Tokens auto-refresh when expired |

---

## User Accounts & Access Control

**Authentication** is required for all pages. Unauthenticated requests redirect to `/login/`.

**Registration** is open — any visitor can create an account at `/register/`.

**Dashboards** are strictly user-scoped. A user only sees, creates, edits, and deletes dashboards they own.

**Projects** are open to all authenticated users. Any logged-in user can:
- View any project
- Add any project to their own dashboards
- Create, rename, and delete projects
- Edit project settings

The `owner` field on a project records who created it (for display and audit purposes) but does not gate access.

**Google OAuth tokens** are per-user per-project. Connecting Google Drive on a project only grants Drive access for the connecting user — other users on the same project must connect their own accounts.

---

## Pages & Features

### Dashboards Home
**URL:** `/`

The landing page after login. Lists all dashboards owned by the current user.

- **Create a dashboard** — inline name input, immediately added to the list
- **Rename a dashboard** — click the dashboard name
- **Delete a dashboard** — removes the dashboard but not its projects
- **Orphaned projects panel** — shows projects you own that are not on any of your dashboards, with a quick "Add to dashboard" control
- Each dashboard card shows a summary: project count, total milestones, completion rate, open risks

### Dashboard View
**URL:** `/dashboard/<id>/`

A focused view of one dashboard's projects.

- Summary stats across all projects on the dashboard: total milestones, completion rate, upcoming milestones (next 60 days), open risks
- Project cards with inline progress bars, event counts, and risk indicators
- **Add project to dashboard** — searchable dropdown of all projects
- **Remove project from dashboard** — per-card remove button
- **Create a new project** — instantly creates and opens the project tracker
- **Navigate to analysis** — link to the cross-project analysis view pre-loaded with this dashboard's projects

### Project Tracker
**URL:** `/project/<id>/`

The core view for a single project. Two panels: Milestones and Events.

#### Milestones
- Filterable by status (all / pending / in-progress / complete) and category
- Each milestone shows: title, date, status badge, category, owner, source link
- **Add milestone** — modal form with title, date, status, category, owner, description, source
- **Edit milestone** — click any milestone to open the edit modal
- **Cycle status** — click the status badge to step through `pending → in-progress → complete`
- **Delete milestone** — from the edit modal
- Summary strip: total count, complete count, in-progress count, completion percentage

#### Events
- Filterable by type (all / hire / depart / reorg / tech / risk / note)
- Each event shows: type badge, title, date, people, owner, source link
- **Add event** — modal with title, date, type, people, owner, description, source
- **Edit event** — click any event to open the edit modal
- **Resolve risk** — for `risk` type events, a resolve button marks them resolved (struck-through)
- **Delete event** — from the edit modal
- Open risk count displayed in the header stats

#### Header controls
- Click the project name to rename it inline
- **⚙ Settings** button links to project settings
- **+ Event** and **+ Milestone** buttons open their respective modals

### Project Settings
**URL:** `/project/<id>/settings/`

A sidebar-navigated settings page with four sections.

#### General
- **Project name** — editable
- **Description** — free-text textarea

Changes are held until **Save Changes** is clicked in the sticky bottom bar. Navigating away with unsaved changes triggers a browser warning.

#### Integrations
Configure Google OAuth for Drive access.

- **Client ID** and **Client Secret** fields — obtained from Google Cloud Console
- The exact **Authorised redirect URI** is displayed with a Copy button — this must be registered verbatim in Google Cloud Console
- **Connect Google Drive** — initiates the OAuth 2.0 consent flow
- **Reconnect / Disconnect** — manage the stored token
- Connection status indicator (connected / not connected)
- **Drive Folder** — folder name (display label) and folder ID fields. The folder ID is found in the Drive URL: `drive.google.com/drive/folders/<FOLDER_ID>`

#### Drive Files
Visible once OAuth credentials and a folder ID are configured. Automatically loads on page open.

- Lists files in the linked Drive folder: icon, name (linked to open in Drive), type, last modified date
- **Filter** — client-side search by filename
- **Browse subfolders** — click the Browse → button on any folder row to drill in
- **Pagination** — Next / Back for folders with more than 50 files
- **Refresh** — re-fetches from Drive
- Clear error messages when the token has expired (prompts to reconnect) or credentials are missing

#### About
- Milestone count, event count, number of your dashboards that include this project
- Creation date and owner
- List of your dashboards that feature this project, with links
- Quick **Add to Dashboard** control if the project is not on any of your dashboards yet

#### Danger Zone
- **Delete project** — permanently deletes the project and all its milestones and events, with a confirmation dialog

### Cross-Project Analysis
**URL:** `/analysis/?p=<id>&p=<id>&...`

Up to 8 projects can be compared side by side. Accessible from any dashboard view or directly via URL.

Seven tabs:

| Tab | Description |
|---|---|
| **Overview** | Comparison table with progress bars, milestone counts, event counts, open risk counts, and date spans |
| **Timeline** | Shared date axis with colour-coded milestone dots per status. Today marker. Hover tooltips. |
| **Activity** | 24-month bar chart per project showing combined milestone and event activity over time |
| **Categories** | Matrix of milestone categories (rows) vs projects (columns) with mini bar fills |
| **Events** | Heatmap of event types per project |
| **Owners** | Owner activity table across projects showing milestone and event ownership |
| **Risks** | Cards per project: open risks (highlighted) and resolved risks (struck through) |

---

## API Reference

All endpoints require authentication (session cookie). All write endpoints accept and return JSON.

### Dashboards

| Method | URL | Description |
|---|---|---|
| POST | `/api/dashboards/` | Create a dashboard |
| PATCH | `/api/dashboards/<id>/rename/` | Rename a dashboard |
| DELETE | `/api/dashboards/<id>/delete/` | Delete a dashboard |
| POST | `/api/dashboards/<id>/projects/` | Add a project to a dashboard |
| DELETE | `/api/dashboards/<id>/projects/<project_id>/` | Remove a project from a dashboard |

### Projects

| Method | URL | Description |
|---|---|---|
| POST | `/api/projects/` | Create a project |
| PATCH | `/api/projects/<id>/rename/` | Rename a project |
| DELETE | `/api/projects/<id>/delete/` | Delete a project and all its data |
| POST | `/api/projects/<id>/settings/` | Save project settings (name, description, OAuth credentials, folder) |

### Milestones

| Method | URL | Description |
|---|---|---|
| GET | `/api/projects/<id>/milestones/` | List all milestones for a project |
| POST | `/api/projects/<id>/milestones/` | Create a milestone |
| PUT | `/api/projects/<id>/milestones/<mid>/` | Update a milestone |
| DELETE | `/api/projects/<id>/milestones/<mid>/` | Delete a milestone |
| PATCH | `/api/projects/<id>/milestones/<mid>/cycle/` | Cycle milestone status (pending → in-progress → complete) |

### Events

| Method | URL | Description |
|---|---|---|
| GET | `/api/projects/<id>/events/` | List all events for a project |
| POST | `/api/projects/<id>/events/` | Create an event |
| PUT | `/api/projects/<id>/events/<eid>/` | Update an event |
| DELETE | `/api/projects/<id>/events/<eid>/` | Delete an event |
| PATCH | `/api/projects/<id>/events/<eid>/resolve/` | Toggle resolved status on a risk event |

### Google Drive

| Method | URL | Description |
|---|---|---|
| GET | `/api/projects/<id>/drive/files/` | List files in the linked Drive folder. Accepts `?folderId=` to browse subfolders and `?pageToken=` for pagination. |
| GET | `/api/projects/<id>/drive/oauth/start/` | Redirect to Google OAuth consent screen |
| GET | `/api/projects/<id>/drive/oauth/callback/` | Google redirects here after consent. Exchanges code for tokens. |
| POST | `/api/projects/<id>/drive/oauth/disconnect/` | Revoke and delete the stored token |

---

## Google Drive Integration

Drive integration uses OAuth 2.0, which allows access to private files without requiring them to be publicly shared.

### Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create an **OAuth 2.0 Client ID** — application type: **Web application**
3. Under **Authorised redirect URIs**, add the exact URI shown in the project's Settings → Integrations page. It follows the pattern: `http://<your-host>/api/projects/<id>/drive/oauth/callback/`
4. Enable the **Google Drive API** for your project in the Cloud Console
5. Copy the **Client ID** and **Client Secret** into the project settings and save
6. Click **Connect Google Drive** — complete the Google consent screen
7. Set the **Folder ID** (found in the Drive URL when you open the folder) and save

### Token handling

- Tokens are stored per-user per-project in the `GoogleOAuthToken` table
- Access tokens auto-refresh using the stored refresh token when they expire
- If a refresh fails (e.g. the user revoked access), the token is deleted and the UI prompts the user to reconnect
- Each user on a project must connect their own Google account

### Troubleshooting

**`token_exchange_failed`** — the redirect URI sent to Google does not exactly match what is registered in Cloud Console. The error message now includes the exact URI used and the full Google error description. Copy the URI from the settings page and paste it verbatim into Cloud Console.

If Django is running behind a proxy and `build_absolute_uri` produces the wrong scheme or host, override it in `settings.py`:

```python
GOOGLE_OAUTH_REDIRECT_BASE = 'https://myapp.example.com'
```

---

## Seed Data

```bash
python manage.py seed_org
```

Creates a 60-person fictional organisation (Acme Corp) with:
- 3 login accounts (`jordan.ellis`, `marcus.webb`, `rachel.torres` — all password: `password`)
- 10 projects spanning January 2024 to December 2025
- Milestones, events, hires, departures, risks, and tech decisions across all projects
- 3 dashboards scoped to different organisational levels (IC, Manager, Director)

The seed command clears all existing dashboards and projects before re-creating them.

---

## Configuration

Key settings in `claro_historia/settings.py`:

```python
# Redirect users to login if not authenticated
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# Override Django's auto-detected base URL for OAuth redirect URIs.
# Set this if running behind a reverse proxy or if the OAuth callback
# is registering the wrong scheme (http vs https) or hostname.
# Example: GOOGLE_OAUTH_REDIRECT_BASE = 'https://myapp.example.com'
GOOGLE_OAUTH_REDIRECT_BASE = ''
```

---

## Migrations

| Migration | Description |
|---|---|
| `0001_initial` | Project, Milestone, Event tables |
| `0002_dashboard` | Dashboard and DashboardProject tables |
| `0003_event_resolved` | `resolved` field on Event |
| `0004_owner` | `owner` CharField on Milestone and Event |
| `0005_milestone_dates` | `date_started` and `date_completed` on Milestone |
| `0006_user_ownership` | `owner` FK (User) on Dashboard and Project |
| `0007_project_settings_fields` | `description`, `google_api_key`, `google_drive_folder_id/name`, `created_at` on Project |
| `0008_oauth` | Renames `google_api_key` → `google_client_id`, adds `google_client_secret`, creates `GoogleOAuthToken` table |

Run all migrations with:

```bash
python manage.py migrate
```
