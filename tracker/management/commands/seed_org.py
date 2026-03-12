"""
seed_org — Acme Corp (60-person org, 10 projects, 2 years, 3 dashboards)

Org structure
─────────────
DIRECTOR:   Rachel Torres  (Engineering + Product Platform)
  MANAGER:  Marcus Webb    (Platform Engineering, 8 ICs)
    ICs:    Priya Nair, Dae-Jung Kim, Sofía Ibarra, Tom Ashford,
            Yuki Tanaka, Lena Fischer, Omar Osei, Ravi Patel
  MANAGER:  Claire Bouchard (Product, 8 ICs)
    ICs:    James Okafor, Mei Lin, Andrés Vargas, Zoe Mitchell,
            Fatima Al-Hassan, Liam Brennan, Ingrid Svensson, Ben Carter

DIRECTOR:   David Okonkwo  (Data & Analytics)
  MANAGER:  Anya Sokolova  (Data Engineering, 7 ICs)
    ICs:    Hiro Nakamura, Selena Cruz, Patrick Mbeki, Nina Kovač,
            Theo Papadopoulos, Amara Diallo, Will Chen
  MANAGER:  Sanjay Mehta   (Data Science, 7 ICs)
    ICs:    Layla Osei, Finn Larsen, Chioma Eze, Max Brauer,
            Yara Salameh, Diego Reyes, Chloe Park

DIRECTOR:   Isla McGregor  (Design & UX)
  MANAGER:  Felix Wagner   (UX Design, 7 ICs)
    ICs:    Rosa Ferreira, Jin-ho Choi, Astrid Lindqvist, Mateo Ruiz,
            Leila Ahmadi, Sam Osei, Tanya Petrova
  MANAGER:  Nadia Obi      (Brand & Content, 6 ICs)
    ICs:    Kwame Asante, Lucia Vidal, Ethan Park, Mia Johansson,
            Carlos Mendes, Freya Nielsen

DIRECTOR:   Amir Hassan    (Marketing & Growth)
  MANAGER:  Olivia Grant   (Growth, 5 ICs)
    ICs:    Tyler Rhodes, Simone Duval, Riku Yamamoto, Pita Havili, Zara King

INDIVIDUAL CONTRIBUTOR (cross-functional):  Jordan Ellis (Senior Engineer, Marcus's team)

Total named: 60 (4 directors, 5 managers, 51 ICs)

Projects (2024-01 → 2025-12)
──────────────────────────────
 1. Core Platform Rebuild            (Platform Eng)           2024-01 → 2025-06
 2. Customer Data Platform           (Data Eng + Platform)    2024-03 → 2025-03
 3. Design System 2.0                (Design + Product)       2024-02 → 2024-11
 4. Mobile App Launch                (Product + Platform)     2024-04 → 2025-02
 5. ML Recommendation Engine         (Data Science)           2024-06 → 2025-09
 6. Brand Refresh                    (Brand + Marketing)      2024-01 → 2024-08
 7. Self-Serve Analytics Dashboard   (Data + Product)         2024-09 → 2025-06
 8. Growth Experimentation Platform  (Growth + Platform)      2024-07 → 2025-04
 9. Enterprise SSO & Compliance      (Platform Eng)           2025-01 → 2025-12
10. Content & SEO Overhaul           (Brand + Growth)         2025-03 → 2025-12

Dashboards
───────────
A. Jordan Ellis — IC view   (projects 1, 2, 4, 8)
B. Marcus Webb  — Manager   (projects 1, 2, 4, 8, 9)
C. Rachel Torres — Director (projects 1, 2, 4, 8, 9 + cross-org 3, 5, 7)
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tracker.models import Dashboard, DashboardProject, Project, Milestone, Event


class Command(BaseCommand):
    help = 'Seeds a 60-person org with 10 projects spanning 2 years and 3 dashboards'

    # Org users: username → (first, last, password)
    USERS = {
        'jordan.ellis':   ('Jordan',  'Ellis',    'password'),
        'marcus.webb':    ('Marcus',  'Webb',     'password'),
        'rachel.torres':  ('Rachel',  'Torres',   'password'),
    }

    def handle(self, *args, **options):
        self.stdout.write('Clearing existing data…')
        Dashboard.objects.all().delete()
        Project.objects.all().delete()

        # Create users
        self._users = {}
        for username, (first, last, pwd) in self.USERS.items():
            user, created = User.objects.get_or_create(username=username)
            if created or True:
                user.first_name = first
                user.last_name = last
                user.set_password(pwd)
                user.save()
            self._users[username] = user
            self.stdout.write(f'  ✓ User: {username}')

        # Marcus owns all platform/product projects (his team's work)
        # Rachel owns the same + cross-org (director scope)
        # Jordan owns the projects he contributed to (IC scope)
        # We use Marcus as the primary project owner since he's the manager;
        # dashboards then provide each person's scoped view.
        marcus  = self._users['marcus.webb']
        rachel  = self._users['rachel.torres']
        jordan  = self._users['jordan.ellis']

        projects = {}
        proj_owners = {
            '_project_platform_rebuild':   'marcus.webb',
            '_project_cdp':                'marcus.webb',
            '_project_design_system':      'rachel.torres',
            '_project_mobile_app':         'marcus.webb',
            '_project_ml_reco':            'rachel.torres',
            '_project_brand_refresh':      'rachel.torres',
            '_project_self_serve_analytics': 'rachel.torres',
            '_project_growth_exp':         'marcus.webb',
            '_project_sso_compliance':     'marcus.webb',
            '_project_content_seo':        'rachel.torres',
        }
        for fn_name in proj_owners:
            owner = self._users[proj_owners[fn_name]]
            proj = getattr(self, fn_name)(owner)
            projects[fn_name] = proj
            self.stdout.write(f'  ✓ {proj.name}')

        self._seed_dashboards(projects)

        self.stdout.write('')
        self.stdout.write('  Login credentials (all passwords: password)')
        for username in self.USERS:
            self.stdout.write(f'    {username}')
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'\nDone. '
            f'{Project.objects.count()} projects · '
            f'{Milestone.objects.count()} milestones · '
            f'{Event.objects.count()} events · '
            f'{Dashboard.objects.count()} dashboards'
        ))

    # ─────────────────────────────────────────────────────────────────────────
    def _ms(self, project, items):
        for d in items:
            Milestone.objects.create(project=project, **d)

    def _ev(self, project, items):
        for d in items:
            Event.objects.create(project=project, **d)

    # =========================================================================
    # PROJECT 1 — Core Platform Rebuild
    # =========================================================================
    def _project_platform_rebuild(self, owner):
        p = Project.objects.create(name='Core Platform Rebuild', owner=owner)
        self._ms(p, [
            dict(title='Architecture Review & Decision Record', date='2024-01-15', status='complete',
                 cat='Architecture', owner='Marcus Webb',
                 source='https://docs.google.com/document/d/arch-review-2024', source_name='ADR-001',
                 desc='Evaluated monolith-to-microservices migration. Decision: modular monolith first, extract services incrementally. Reduces initial risk by 60%.'),
            dict(title='Development Environment Standardisation', date='2024-02-05', status='complete',
                 cat='Infrastructure', owner='Priya Nair',
                 source='https://github.com/acme/platform/pull/12', source_name='PR #12 — Dev Env',
                 desc='Unified Docker Compose setup, shared .env templates, and pre-commit hooks rolled out to all 8 platform engineers.'),
            dict(title='CI/CD Pipeline v2', date='2024-03-01', status='complete',
                 cat='Infrastructure', owner='Dae-Jung Kim',
                 source='https://github.com/acme/platform/pull/38', source_name='PR #38 — CI/CD',
                 desc='GitHub Actions pipeline replaces legacy Jenkins. Build time cut from 18 min to 6 min. Parallel test sharding introduced.'),
            dict(title='Database Schema Migration — Phase 1', date='2024-04-12', status='complete',
                 cat='Engineering', owner='Sofía Ibarra',
                 source='https://docs.google.com/document/d/db-migration-phase1', source_name='DB Migration Plan',
                 desc='Core user, account, and billing tables migrated to new schema. Zero-downtime deployment using expand-contract pattern.'),
            dict(title='API Gateway Implementation', date='2024-05-20', status='complete',
                 cat='Engineering', owner='Tom Ashford',
                 source='https://github.com/acme/platform/pull/87', source_name='PR #87 — API Gateway',
                 desc='Kong-based gateway introduced. Rate limiting, auth middleware, and request logging centralised. Replaced 4 ad-hoc auth implementations.'),
            dict(title='Observability Stack (Metrics + Tracing)', date='2024-06-14', status='complete',
                 cat='Infrastructure', owner='Yuki Tanaka',
                 source='https://docs.google.com/document/d/observability-spec', source_name='Observability Spec',
                 desc='Prometheus + Grafana + Tempo deployed. SLOs defined for all 12 core services. First on-call runbooks published.'),
            dict(title='Auth Service Extraction', date='2024-07-26', status='complete',
                 cat='Engineering', owner='Jordan Ellis',
                 source='https://github.com/acme/platform/pull/134', source_name='PR #134 — Auth Service',
                 desc='Auth extracted as standalone service. OAuth 2.0 + PKCE implemented. Session management centralised. 99.99% uptime in first 30 days.'),
            dict(title='Database Schema Migration — Phase 2', date='2024-09-06', status='complete',
                 cat='Engineering', owner='Sofía Ibarra',
                 source='https://docs.google.com/document/d/db-migration-phase2', source_name='DB Migration Phase 2',
                 desc='Content, analytics, and notification tables migrated. Deprecated 3 legacy tables. Query performance improved 40% on average.'),
            dict(title='Notification Service', date='2024-10-18', status='complete',
                 cat='Engineering', owner='Lena Fischer',
                 source='https://github.com/acme/platform/pull/201', source_name='PR #201 — Notifications',
                 desc='Email, in-app, and push notifications unified. Template system introduced. Unsubscribe management integrated with GDPR controls.'),
            dict(title='Billing Service Extraction', date='2024-12-06', status='complete',
                 cat='Engineering', owner='Omar Osei',
                 source='https://github.com/acme/platform/pull/247', source_name='PR #247 — Billing',
                 desc='Stripe integration migrated to dedicated service. Webhook reliability improved — failure rate from 2.3% to 0.04%.'),
            dict(title='Load Testing & Capacity Planning', date='2025-01-17', status='complete',
                 cat='QA', owner='Ravi Patel',
                 source='https://docs.google.com/spreadsheets/d/load-test-results', source_name='Load Test Results',
                 desc='Simulated 10× peak traffic. Identified 3 bottlenecks. Auto-scaling rules updated. System now certified for 500k daily active users.'),
            dict(title='Platform Security Hardening', date='2025-02-28', status='complete',
                 cat='Security', owner='Priya Nair',
                 source='https://docs.google.com/document/d/security-audit-2025', source_name='Security Audit Report',
                 desc='External pen test by Cure53. 2 high, 6 medium findings. All resolved within 3 weeks. Secret scanning and dependency audit automated.'),
            dict(title='Developer Documentation & SDK', date='2025-04-11', status='in-progress',
                 cat='Documentation', owner='Tom Ashford',
                 source='https://notion.so/acme/platform-sdk-docs', source_name='SDK Docs — Notion',
                 desc='Public API reference, getting-started guide, and Python/JS SDKs. Target: 80% of endpoints documented by April 30.'),
            dict(title='Platform v2.0 GA Release', date='2025-06-13', status='pending',
                 cat='Launch', owner='Marcus Webb',
                 source='https://docs.google.com/document/d/platform-v2-launch-plan', source_name='Launch Plan',
                 desc='Full cutover from legacy platform. Deprecation notices to be sent 60 days prior. Migration guides for all internal consumers.'),
        ])
        self._ev(p, [
            dict(title='Marcus Webb joins as Platform Engineering Manager', date='2024-01-08', etype='hire',
                 people='Marcus Webb', owner='Rachel Torres',
                 desc='Marcus brings 10 years of distributed systems experience from Stripe and Cloudflare.'),
            dict(title='Jordan Ellis promoted to Senior Engineer', date='2024-01-22', etype='reorg',
                 people='Jordan Ellis', owner='Marcus Webb',
                 desc='Promoted in recognition of platform leadership over the previous 18 months.'),
            dict(title='Ravi Patel joins as Platform Engineer', date='2024-03-04', etype='hire',
                 people='Ravi Patel', owner='Marcus Webb',
                 desc='Ravi joins from AWS with expertise in distributed systems and chaos engineering.'),
            dict(title='Legacy API v1 deprecation announced', date='2024-05-01', etype='note',
                 people='Marcus Webb, Tom Ashford', owner='Marcus Webb',
                 desc='All internal consumers notified. 6-month migration window agreed. 11 of 14 services already on v2.'),
            dict(title='Production incident — Auth service memory leak', date='2024-08-14', etype='risk',
                 people='Jordan Ellis, Dae-Jung Kim', owner='Jordan Ellis',
                 desc='P0 incident. 47-minute partial outage for EU customers. Root cause: connection pool not released under retry storm. Hotfix deployed in 2 hours.',
                 resolved=True),
            dict(title='Lena Fischer on parental leave', date='2024-11-01', etype='note',
                 people='Lena Fischer', owner='Marcus Webb',
                 desc='Lena returns Q1 2025. Notification service work handed off to Omar Osei.'),
            dict(title='External security audit — Cure53 engaged', date='2025-01-06', etype='tech',
                 people='Priya Nair, Marcus Webb', owner='Priya Nair',
                 desc='Two-week engagement. Scope: API gateway, auth service, and billing service.'),
            dict(title='Platform budget overrun risk', date='2025-03-10', etype='risk',
                 people='Marcus Webb, Rachel Torres', owner='Rachel Torres',
                 desc='Cloud infrastructure costs tracking 18% above Q1 budget due to load testing environment. Cost optimisation sprint planned for April.',
                 resolved=False),
            dict(title='Lena Fischer returns from parental leave', date='2025-03-17', etype='hire',
                 people='Lena Fischer', owner='Marcus Webb',
                 desc='Lena returns full-time. Onboarding to billing service work.'),
            dict(title='Platform Eng team offsite — Berlin', date='2025-04-02', etype='note',
                 people='Marcus Webb, Jordan Ellis, Priya Nair, Dae-Jung Kim, Sofía Ibarra, Tom Ashford, Yuki Tanaka, Lena Fischer, Omar Osei, Ravi Patel',
                 owner='Marcus Webb',
                 desc='3-day offsite. Roadmap planning, team retrospective, and hands-on workshops on observability tooling.'),
        ])
        return p

    # =========================================================================
    # PROJECT 2 — Customer Data Platform
    # =========================================================================
    def _project_cdp(self, owner):
        p = Project.objects.create(name='Customer Data Platform', owner=owner)
        self._ms(p, [
            dict(title='CDP Requirements & Vendor Evaluation', date='2024-03-08', status='complete',
                 cat='Planning', owner='Anya Sokolova',
                 source='https://docs.google.com/spreadsheets/d/cdp-vendor-eval', source_name='Vendor Comparison Matrix',
                 desc='Evaluated Segment, RudderStack, and custom build. Decision: RudderStack self-hosted for data sovereignty and cost.'),
            dict(title='Data Warehouse Selection (Snowflake)', date='2024-03-22', status='complete',
                 cat='Infrastructure', owner='Sanjay Mehta',
                 source='https://docs.google.com/document/d/snowflake-adr', source_name='Snowflake ADR',
                 desc='Snowflake selected over BigQuery and Redshift. Key factors: time-travel, data sharing, and existing team expertise.'),
            dict(title='Event Schema Design & Taxonomy', date='2024-04-19', status='complete',
                 cat='Architecture', owner='Hiro Nakamura',
                 source='https://docs.google.com/document/d/event-taxonomy', source_name='Event Taxonomy v1',
                 desc='120 event types defined across web, mobile, and API surfaces. Naming conventions and validation rules documented.'),
            dict(title='Ingestion Pipeline — Web & Mobile', date='2024-05-31', status='complete',
                 cat='Engineering', owner='Jordan Ellis',
                 source='https://github.com/acme/cdp/pull/29', source_name='PR #29 — Web Ingestion',
                 desc='RudderStack SDKs integrated into web app and iOS/Android. 99.7% event delivery rate in first week. ~2M events/day at launch.'),
            dict(title='dbt Transformation Layer', date='2024-07-05', status='complete',
                 cat='Engineering', owner='Selena Cruz',
                 source='https://github.com/acme/cdp-dbt', source_name='CDP dbt Repo',
                 desc='42 dbt models built. User identity resolution, funnel tables, and revenue attribution included. Documentation coverage 90%.'),
            dict(title='Identity Resolution & User Stitching', date='2024-08-16', status='complete',
                 cat='Engineering', owner='Patrick Mbeki',
                 source='https://docs.google.com/document/d/identity-resolution', source_name='Identity Resolution Design',
                 desc='Cross-device and cross-session identity graph built. Match rate 78% for logged-in users, 34% for anonymous.'),
            dict(title='Marketing & CRM Integrations', date='2024-09-27', status='complete',
                 cat='Integration', owner='Amara Diallo',
                 source='https://docs.google.com/document/d/integrations-spec', source_name='Integration Spec',
                 desc='Salesforce, HubSpot, Intercom, and Braze connected. Audience sync latency under 15 minutes.'),
            dict(title='Data Quality Framework & Monitoring', date='2024-11-08', status='complete',
                 cat='Quality', owner='Nina Kovač',
                 source='https://docs.google.com/document/d/data-quality-framework', source_name='Data Quality Framework',
                 desc='Great Expectations suite covering 180 data quality checks. Alerting on schema drift and volume anomalies. 3 regressions caught in first month.'),
            dict(title='Self-Serve Audience Builder (Beta)', date='2025-01-10', status='complete',
                 cat='Product', owner='Mei Lin',
                 source='https://www.figma.com/file/audience-builder', source_name='Figma — Audience Builder',
                 desc='Beta launched to Marketing team. 12 audiences created in first week. 3 A/B tests launched on day 1.'),
            dict(title='GDPR & Data Retention Policies', date='2025-02-14', status='complete',
                 cat='Compliance', owner='Anya Sokolova',
                 source='https://docs.google.com/document/d/gdpr-cdp', source_name='GDPR Compliance Checklist',
                 desc='Right-to-erasure pipeline: full deletion within 30 days. Retention policies applied to all 120 event types. DPA updated.'),
            dict(title='CDP General Availability', date='2025-03-07', status='complete',
                 cat='Launch', owner='Anya Sokolova',
                 source='https://docs.google.com/document/d/cdp-ga-announcement', source_name='CDP GA Announcement',
                 desc='CDP opened to all internal teams. 6 business units onboarded in first month. Processing 8M events/day at GA.'),
        ])
        self._ev(p, [
            dict(title='Hiro Nakamura joins as Senior Data Engineer', date='2024-03-04', etype='hire',
                 people='Hiro Nakamura', owner='Anya Sokolova',
                 desc='Hiro joins from Shopify Data with expertise in Kafka and dbt. Leads event schema work.'),
            dict(title='Data pipeline outage — Snowflake credit exhaustion', date='2024-06-12', etype='risk',
                 people='Selena Cruz, Anya Sokolova', owner='Anya Sokolova',
                 desc='Runaway query consumed 2,400 credits overnight. 6-hour data gap in analytics. Credit alerts and query governance rules implemented.',
                 resolved=True),
            dict(title='Patrick Mbeki promoted to Staff Engineer', date='2024-07-15', etype='reorg',
                 people='Patrick Mbeki', owner='Anya Sokolova',
                 desc='Promoted following identity resolution architecture work. First Staff Engineer in Data Eng team.'),
            dict(title='Marketing team onboarded to CDP', date='2024-10-01', etype='note',
                 people='Olivia Grant, Simone Duval, Amara Diallo', owner='Anya Sokolova',
                 desc='2-day training workshop. 18 Marketing staff now active CDP users. 4 new audience segments created on day 1.'),
            dict(title='GDPR erasure SLA risk — manual backlog', date='2024-12-02', etype='risk',
                 people='Nina Kovač, Anya Sokolova', owner='Anya Sokolova',
                 desc='Erasure pipeline handling <60% of requests within 30-day SLA. Automated backlog processor built and deployed in sprint 24.',
                 resolved=True),
            dict(title='CDP Steering Committee formed', date='2025-01-13', etype='reorg',
                 people='David Okonkwo, Anya Sokolova, Sanjay Mehta, Claire Bouchard', owner='David Okonkwo',
                 desc='Cross-functional committee to govern CDP roadmap, data access policies, and integration prioritisation. Monthly cadence.'),
        ])
        return p

    # =========================================================================
    # PROJECT 3 — Design System 2.0
    # =========================================================================
    def _project_design_system(self, owner):
        p = Project.objects.create(name='Design System 2.0', owner=owner)
        self._ms(p, [
            dict(title='Audit of Existing Components', date='2024-02-09', status='complete',
                 cat='Research', owner='Felix Wagner',
                 source='https://www.figma.com/file/ds-audit', source_name='Figma — DS Audit',
                 desc='182 existing components audited. 34% flagged as duplicates or deprecated. 12 critical accessibility gaps identified.'),
            dict(title='Token Architecture Design', date='2024-03-01', status='complete',
                 cat='Design', owner='Rosa Ferreira',
                 source='https://www.figma.com/file/token-system', source_name='Figma — Token System',
                 desc='3-tier token system: global → semantic → component. 240 design tokens defined. Dark mode and high-contrast themes supported from day 1.'),
            dict(title='Core Component Library (Figma)', date='2024-04-12', status='complete',
                 cat='Design', owner='Jin-ho Choi',
                 source='https://www.figma.com/file/ds2-components', source_name='Figma — DS 2.0 Components',
                 desc='68 production-ready components. Auto-layout, interactive variants, and annotation layers included. Published to Figma Community.'),
            dict(title='React Component Library — v1.0', date='2024-05-24', status='complete',
                 cat='Engineering', owner='Astrid Lindqvist',
                 source='https://github.com/acme/ui', source_name='GitHub — acme/ui',
                 desc='npm package @acme/ui published. Storybook with 100% component coverage. Chromatic visual regression testing integrated.'),
            dict(title='Migration Guide & Tooling', date='2024-06-28', status='complete',
                 cat='Documentation', owner='Mateo Ruiz',
                 source='https://notion.so/acme/ds2-migration-guide', source_name='Migration Guide',
                 desc='Codemods for 40 most common component swaps. Interactive migration tracker. Office hours held every Friday during migration window.'),
            dict(title='Web App Migration (70% coverage)', date='2024-08-09', status='complete',
                 cat='Engineering', owner='Felix Wagner',
                 source='https://github.com/acme/app/pull/312', source_name='PR #312 — DS2 Migration',
                 desc='Core product surfaces migrated. 714 component instances updated. Visual regression suite now covers 230 screens.'),
            dict(title='Accessibility Audit (WCAG 2.2 AA)', date='2024-09-13', status='complete',
                 cat='QA', owner='Leila Ahmadi',
                 source='https://docs.google.com/document/d/ds2-a11y-audit', source_name='A11y Audit Report',
                 desc='All 68 components pass WCAG 2.2 AA. axe-core integrated into Storybook and CI. Focus management and ARIA patterns documented.'),
            dict(title='Design System 2.0 — Official Launch', date='2024-10-04', status='complete',
                 cat='Launch', owner='Isla McGregor',
                 source='https://docs.google.com/presentation/d/ds2-launch-deck', source_name='DS 2.0 Launch Deck',
                 desc='Company-wide launch. 30+ engineers and 8 designers trained. Legacy DS1 deprecated with 6-month sunset window.'),
            dict(title='Full Web App Migration (100% coverage)', date='2024-11-15', status='complete',
                 cat='Engineering', owner='Felix Wagner',
                 source='https://github.com/acme/app/pull/418', source_name='PR #418 — DS2 Full Migration',
                 desc='Final 30% of product surfaces migrated. DS1 removed from codebase. Bundle size reduced 22%. Theme switching works across entire product.'),
        ])
        self._ev(p, [
            dict(title='Leila Ahmadi joins as Accessibility Specialist', date='2024-02-12', etype='hire',
                 people='Leila Ahmadi', owner='Felix Wagner',
                 desc='Leila joins from Shopify Accessibility team. First dedicated accessibility role at Acme.'),
            dict(title='DS 1.0 — critical colour contrast failures found', date='2024-03-15', etype='risk',
                 people='Leila Ahmadi, Felix Wagner', owner='Felix Wagner',
                 desc='Accessibility audit revealed 14 WCAG AA contrast failures in DS1. Emergency patch to DS1 released; resolved properly in DS2.',
                 resolved=True),
            dict(title='Engineering partnership programme launched', date='2024-05-06', etype='note',
                 people='Felix Wagner, Marcus Webb, Claire Bouchard', owner='Felix Wagner',
                 desc='Each product squad assigned a Design System liaison engineer. Accelerates adoption and surfaces edge cases earlier.'),
            dict(title='DS 2.0 wins internal Innovation Award', date='2024-11-22', etype='note',
                 people='Felix Wagner, Rosa Ferreira, Jin-ho Choi, Astrid Lindqvist', owner='Isla McGregor',
                 desc='Quarterly innovation award voted by the company. 94% of engineers rate DS2 as "significantly better" than DS1.'),
        ])
        return p

    # =========================================================================
    # PROJECT 4 — Mobile App Launch
    # =========================================================================
    def _project_mobile_app(self, owner):
        p = Project.objects.create(name='Mobile App Launch', owner=owner)
        self._ms(p, [
            dict(title='Mobile Strategy & Scope Definition', date='2024-04-05', status='complete',
                 cat='Planning', owner='Claire Bouchard',
                 source='https://docs.google.com/document/d/mobile-strategy', source_name='Mobile Strategy Doc',
                 desc='React Native selected for cross-platform efficiency. MVP scope: core dashboard, notifications, and quick actions. Native feel for iOS and Android.'),
            dict(title='React Native Architecture & Dev Setup', date='2024-05-10', status='complete',
                 cat='Engineering', owner='Jordan Ellis',
                 source='https://github.com/acme/mobile/pull/1', source_name='PR #1 — RN Architecture',
                 desc='Monorepo setup, shared component library with web, Expo managed workflow, and over-the-air update strategy agreed.'),
            dict(title='UX Research — Mobile Patterns', date='2024-05-24', status='complete',
                 cat='Research', owner='Zoe Mitchell',
                 source='https://docs.google.com/presentation/d/mobile-ux-research', source_name='Mobile UX Research',
                 desc='16 user sessions on competitor apps. Key insights: biometric auth, offline mode, and widget support are top requests.'),
            dict(title='Mobile Design System (DS2 native extension)', date='2024-06-21', status='complete',
                 cat='Design', owner='Jin-ho Choi',
                 source='https://www.figma.com/file/mobile-ds', source_name='Figma — Mobile DS',
                 desc='84 native mobile components extending DS2. Platform-specific gesture patterns, haptics, and navigation paradigms documented.'),
            dict(title='Core Dashboard — iOS & Android', date='2024-08-02', status='complete',
                 cat='Engineering', owner='Jordan Ellis',
                 source='https://github.com/acme/mobile/pull/67', source_name='PR #67 — Dashboard',
                 desc='Real-time data dashboard with charts, KPI cards, and customisable widget layout. Performance: 60fps on 5-year-old devices.'),
            dict(title='Push Notifications Integration', date='2024-09-06', status='complete',
                 cat='Engineering', owner='Dae-Jung Kim',
                 source='https://github.com/acme/mobile/pull/98', source_name='PR #98 — Push Notifications',
                 desc='APNs and FCM integrated via Platform notification service. Opt-in/opt-out per category. Average delivery time 1.2 seconds.'),
            dict(title='Biometric Authentication', date='2024-09-27', status='complete',
                 cat='Engineering', owner='Priya Nair',
                 source='https://github.com/acme/mobile/pull/112', source_name='PR #112 — Biometric Auth',
                 desc='Face ID, Touch ID, and Android biometrics integrated. Secure enclave key storage. Fallback to PIN with rate limiting.'),
            dict(title='Beta Programme — 200 users', date='2024-10-18', status='complete',
                 cat='QA', owner='James Okafor',
                 source='https://docs.google.com/spreadsheets/d/mobile-beta-feedback', source_name='Beta Feedback Tracker',
                 desc='200 power users across iOS and Android. 47 bugs filed, 42 resolved before GA. NPS: 68 (vs 41 for web).'),
            dict(title='App Store Submission & Review', date='2024-11-08', status='complete',
                 cat='Launch', owner='Andrés Vargas',
                 source='https://docs.google.com/document/d/app-store-submission', source_name='App Store Submission Checklist',
                 desc='iOS and Android submissions simultaneous. Apple review: 5 days (1 rejection resolved in 48h). Google Play: 2 days.'),
            dict(title='Mobile App Public Launch', date='2024-12-06', status='complete',
                 cat='Launch', owner='Claire Bouchard',
                 source='https://docs.google.com/presentation/d/mobile-launch-plan', source_name='Launch Plan',
                 desc='Simultaneous iOS and Android launch. 4,200 downloads in first 48 hours. App Store: 4.6★. Play Store: 4.4★.'),
            dict(title='Offline Mode & Background Sync', date='2025-01-17', status='complete',
                 cat='Engineering', owner='Jordan Ellis',
                 source='https://github.com/acme/mobile/pull/198', source_name='PR #198 — Offline Mode',
                 desc='Core screens work offline. Background sync on reconnect. Conflict resolution for concurrent edits documented.'),
            dict(title='Home Screen Widgets (iOS & Android)', date='2025-02-07', status='complete',
                 cat='Engineering', owner='Tom Ashford',
                 source='https://github.com/acme/mobile/pull/234', source_name='PR #234 — Widgets',
                 desc='3 widget sizes for iOS (WidgetKit) and Android (Glance). KPI snapshot and recent activity widgets. 28% of active users enable at least one widget within 7 days.'),
        ])
        self._ev(p, [
            dict(title='James Okafor joins as Senior Product Manager — Mobile', date='2024-04-08', etype='hire',
                 people='James Okafor', owner='Claire Bouchard',
                 desc='James joins from Meta with 5 years of consumer mobile product experience.'),
            dict(title='Andrés Vargas joins as Mobile Engineer', date='2024-05-13', etype='hire',
                 people='Andrés Vargas', owner='Marcus Webb',
                 desc='Andrés brings iOS native experience (UIKit and SwiftUI). First mobile-specialist hire on the engineering team.'),
            dict(title='Apple App Store rejection — guideline 4.3', date='2024-11-15', etype='risk',
                 people='Andrés Vargas, James Okafor', owner='Andrés Vargas',
                 desc='Rejected for duplicate app claim. Resolved by providing detailed differentiation documentation. Approved on second submission.',
                 resolved=True),
            dict(title='Mobile roadmap Q1 2025 review', date='2025-01-06', etype='note',
                 people='Claire Bouchard, James Okafor, Jordan Ellis', owner='Claire Bouchard',
                 desc='Q1 focus: offline mode, widgets, and tablet optimisation. Tablet support deferred to Q2 pending design resource.'),
            dict(title='10,000 MAU milestone reached', date='2025-02-14', etype='note',
                 people='James Okafor, Claire Bouchard', owner='James Okafor',
                 desc='10,000 monthly active users reached 10 weeks post-launch. Retention D30: 42% (industry benchmark: 30%).'),
        ])
        return p

    # =========================================================================
    # PROJECT 5 — ML Recommendation Engine
    # =========================================================================
    def _project_ml_reco(self, owner):
        p = Project.objects.create(name='ML Recommendation Engine', owner=owner)
        self._ms(p, [
            dict(title='Problem Framing & Success Metrics', date='2024-06-07', status='complete',
                 cat='Planning', owner='Sanjay Mehta',
                 source='https://docs.google.com/document/d/reco-problem-framing', source_name='Problem Framing Doc',
                 desc='Target: 15% uplift in content engagement and 8% increase in feature adoption. Metrics: CTR, session depth, 7-day retention.'),
            dict(title='Data Exploration & Feature Inventory', date='2024-07-05', status='complete',
                 cat='Research', owner='Layla Osei',
                 source='https://github.com/acme/ml-reco/blob/main/notebooks/01_eda.ipynb', source_name='EDA Notebook',
                 desc='82 candidate features identified from CDP. 24 selected for v1 model. User-item interaction matrix: 2.1M users × 3,400 items.'),
            dict(title='Baseline Model (Collaborative Filtering)', date='2024-08-09', status='complete',
                 cat='ML', owner='Finn Larsen',
                 source='https://github.com/acme/ml-reco/pull/18', source_name='PR #18 — Baseline Model',
                 desc='ALS collaborative filtering baseline. Offline: Precision@10 = 0.31, NDCG@10 = 0.44. A/B test designed against rule-based system.'),
            dict(title='Feature Store Implementation', date='2024-09-13', status='complete',
                 cat='Engineering', owner='Chioma Eze',
                 source='https://docs.google.com/document/d/feature-store-design', source_name='Feature Store Design',
                 desc='Feast-based feature store on Snowflake + Redis. Point-in-time correct training and low-latency serving (<20ms P99).'),
            dict(title='Two-Tower Neural Model', date='2024-10-25', status='complete',
                 cat='ML', owner='Max Brauer',
                 source='https://github.com/acme/ml-reco/pull/54', source_name='PR #54 — Two-Tower Model',
                 desc='User tower (128-dim) + Item tower (128-dim). Trained on 90 days of interaction data. Offline NDCG@10 = 0.61 (+39% vs baseline).'),
            dict(title='Online A/B Test — Phase 1', date='2024-12-06', status='complete',
                 cat='Experimentation', owner='Yara Salameh',
                 source='https://docs.google.com/spreadsheets/d/reco-ab-test-p1', source_name='A/B Test Results — Phase 1',
                 desc='10% traffic experiment. Results after 4 weeks: +18% CTR, +11% session depth, +7% D7 retention. All metrics significant at p<0.01.'),
            dict(title='Model Serving Infrastructure', date='2025-01-17', status='complete',
                 cat='Engineering', owner='Diego Reyes',
                 source='https://github.com/acme/ml-reco/pull/89', source_name='PR #89 — Serving Infra',
                 desc='Triton Inference Server on GPU instances. Latency P50: 8ms, P99: 22ms. Auto-scaling configured for peak traffic.'),
            dict(title='Contextual Bandits — Exploration Layer', date='2025-03-07', status='complete',
                 cat='ML', owner='Chloe Park',
                 source='https://docs.google.com/document/d/bandits-design', source_name='Bandits Design Doc',
                 desc='Thompson sampling over item catalogue. Cold-start handled for new items and new users. Exploration rate tuned per user segment.'),
            dict(title='Full Rollout — 100% Traffic', date='2025-04-18', status='in-progress',
                 cat='Launch', owner='Sanjay Mehta',
                 source='https://docs.google.com/document/d/reco-rollout-plan', source_name='Rollout Plan',
                 desc='Graduated rollout: 25% → 50% → 100%. Currently at 50%. Final rollout pending confirmation of infrastructure costs.'),
            dict(title='Personalisation v2 — Cross-Product Signals', date='2025-06-20', status='pending',
                 cat='ML', owner='Finn Larsen',
                 source='https://docs.google.com/document/d/personalisation-v2', source_name='Personalisation v2 Proposal',
                 desc='Incorporate signals from mobile app, email engagement, and CRM data into recommendation context.'),
            dict(title='Model Monitoring & Drift Detection', date='2025-07-25', status='pending',
                 cat='MLOps', owner='Chioma Eze',
                 source='https://notion.so/acme/model-monitoring-plan', source_name='Model Monitoring Plan',
                 desc='Feature drift, prediction distribution, and business metric monitoring. Automated retraining trigger when drift detected.'),
            dict(title='Recommendation Engine v2.0 Release', date='2025-09-12', status='pending',
                 cat='Launch', owner='Sanjay Mehta',
                 desc='Full v2 with contextual bandits, cross-product signals, and drift monitoring. Target: 25% cumulative uplift vs pre-ML baseline.'),
        ])
        self._ev(p, [
            dict(title='Layla Osei joins as ML Engineer', date='2024-06-03', etype='hire',
                 people='Layla Osei', owner='Sanjay Mehta',
                 desc='Layla joins from Google Brain with expertise in recommendation systems and deep learning.'),
            dict(title='GPU training cluster provisioned', date='2024-09-02', etype='tech',
                 people='Diego Reyes, Sanjay Mehta', owner='Diego Reyes',
                 desc='4× A100 GPU cluster on AWS. Monthly cost: $18,400. Training time for full model: 6 hours (vs 3 days on CPU).'),
            dict(title='Training data pipeline failure — 2-week gap', date='2024-11-18', etype='risk',
                 people='Chioma Eze, Hiro Nakamura', owner='Chioma Eze',
                 desc='CDC replication lag caused 2-week gap in training data. Model rolled back to previous checkpoint. Root cause fixed; replication monitoring added.',
                 resolved=True),
            dict(title='A/B test results presented to leadership', date='2025-01-10', etype='note',
                 people='Sanjay Mehta, David Okonkwo, Rachel Torres', owner='Sanjay Mehta',
                 desc='Phase 1 results presented to exec team. Rachel Torres approved full rollout. Additional GPU capacity approved for serving.'),
            dict(title='ML infrastructure cost overrun', date='2025-04-07', etype='risk',
                 people='Diego Reyes, David Okonkwo', owner='David Okonkwo',
                 desc='GPU serving costs tracking 25% above plan at 50% traffic. Spot instance migration and model quantisation being investigated.',
                 resolved=False),
        ])
        return p

    # =========================================================================
    # PROJECT 6 — Brand Refresh
    # =========================================================================
    def _project_brand_refresh(self, owner):
        p = Project.objects.create(name='Brand Refresh', owner=owner)
        self._ms(p, [
            dict(title='Brand Audit & Competitive Landscape', date='2024-01-19', status='complete',
                 cat='Research', owner='Nadia Obi',
                 source='https://docs.google.com/presentation/d/brand-audit', source_name='Brand Audit Deck',
                 desc='Audit of all brand touchpoints: website, social, sales materials, and product UI. 12 competitor brands benchmarked.'),
            dict(title='Brand Strategy & Positioning', date='2024-02-16', status='complete',
                 cat='Strategy', owner='Amir Hassan',
                 source='https://docs.google.com/document/d/brand-strategy', source_name='Brand Strategy Doc',
                 desc='New positioning: "The operating system for ambitious teams." Brand pillars: clarity, momentum, and trust.'),
            dict(title='Visual Identity System', date='2024-03-22', status='complete',
                 cat='Design', owner='Nadia Obi',
                 source='https://www.figma.com/file/visual-identity', source_name='Figma — Visual Identity',
                 desc='New logo, colour palette (expanded from 8 to 22 tokens), typography (Neue Haas Grotesk + iA Writer), and illustration style.'),
            dict(title='Brand Guidelines & Asset Library', date='2024-04-19', status='complete',
                 cat='Documentation', owner='Kwame Asante',
                 source='https://docs.google.com/document/d/brand-guidelines', source_name='Brand Guidelines v1',
                 desc='80-page brand guidelines. 340 assets in Figma. Usage rules, do/don\'t examples, and partner licensing guide included.'),
            dict(title='Website Rebrand', date='2024-05-31', status='complete',
                 cat='Engineering', owner='Lucia Vidal',
                 source='https://github.com/acme/website/pull/78', source_name='PR #78 — Rebrand',
                 desc='New brand applied across all 42 website pages. Launched with zero downtime. Organic search traffic +9% in first 30 days.'),
            dict(title='Social & Marketing Asset Rollout', date='2024-06-21', status='complete',
                 cat='Marketing', owner='Mia Johansson',
                 source='https://docs.google.com/spreadsheets/d/brand-rollout-tracker', source_name='Brand Rollout Tracker',
                 desc='LinkedIn, Twitter/X, email templates, and pitch decks refreshed. Sales team trained on new brand standards.'),
            dict(title='Brand Refresh — Retrospective & Handoff', date='2024-08-02', status='complete',
                 cat='Planning', owner='Nadia Obi',
                 source='https://docs.google.com/document/d/brand-retro', source_name='Brand Refresh Retrospective',
                 desc='Project closed. Brand stewardship handed to Marketing. Quarterly brand health survey established. NPS for brand perception: +22 points.'),
        ])
        self._ev(p, [
            dict(title='Kwame Asante joins as Brand Designer', date='2024-01-15', etype='hire',
                 people='Kwame Asante', owner='Nadia Obi',
                 desc='Kwame joins from Pentagram with consumer and B2B brand expertise.'),
            dict(title='Logo concept rejected by CEO', date='2024-03-04', etype='risk',
                 people='Nadia Obi, Isla McGregor, Amir Hassan', owner='Isla McGregor',
                 desc='Initial logo direction rejected after CEO review. 2-week rework. New direction approved unanimously by exec team.',
                 resolved=True),
            dict(title='External brand agency partnership — Wolff Olins', date='2024-02-01', etype='note',
                 people='Nadia Obi, Amir Hassan', owner='Amir Hassan',
                 desc='Wolff Olins engaged for brand strategy and visual identity. 10-week engagement. Internal team leads execution.'),
            dict(title='Brand launch media coverage', date='2024-06-24', etype='note',
                 people='Amir Hassan, Olivia Grant', owner='Amir Hassan',
                 desc='Coverage in Fast Company, The Drum, and TechCrunch. LinkedIn post: 12,400 impressions, 840 reactions. Website traffic +34% launch week.'),
        ])
        return p

    # =========================================================================
    # PROJECT 7 — Self-Serve Analytics Dashboard
    # =========================================================================
    def _project_self_serve_analytics(self, owner):
        p = Project.objects.create(name='Self-Serve Analytics Dashboard', owner=owner)
        self._ms(p, [
            dict(title='User Research — Analytics Needs', date='2024-09-06', status='complete',
                 cat='Research', owner='Zoe Mitchell',
                 source='https://docs.google.com/presentation/d/analytics-research', source_name='Analytics Research Deck',
                 desc='24 interviews with power users across 6 customer segments. Top needs: custom date ranges, CSV export, and shareable dashboards.'),
            dict(title='Technical Architecture — Query Layer', date='2024-10-04', status='complete',
                 cat='Architecture', owner='Theo Papadopoulos',
                 source='https://docs.google.com/document/d/analytics-query-arch', source_name='Query Architecture ADR',
                 desc='Apache Cube.js semantic layer over Snowflake. Pre-aggregations for common queries. P99 query latency target: <3 seconds.'),
            dict(title='Charting Library Selection', date='2024-10-25', status='complete',
                 cat='Engineering', owner='Fatima Al-Hassan',
                 source='https://docs.google.com/spreadsheets/d/charting-eval', source_name='Charting Library Evaluation',
                 desc='Evaluated Recharts, ECharts, and Observable Plot. ECharts selected for performance and chart variety. DS2 theming applied.'),
            dict(title='Core Charts — Line, Bar, Funnel, Table', date='2024-12-06', status='complete',
                 cat='Engineering', owner='Fatima Al-Hassan',
                 source='https://github.com/acme/analytics/pull/45', source_name='PR #45 — Core Charts',
                 desc='6 chart types implemented. Real-time data refresh (30-second polling). Responsive across desktop, tablet, and mobile.'),
            dict(title='Dashboard Builder — Drag & Drop', date='2025-01-17', status='complete',
                 cat='Engineering', owner='Liam Brennan',
                 source='https://github.com/acme/analytics/pull/78', source_name='PR #78 — Dashboard Builder',
                 desc='React-grid-layout based builder. Save, share (link + embed), and clone dashboards. Up to 20 widgets per dashboard.'),
            dict(title='CSV & PDF Export', date='2025-02-07', status='complete',
                 cat='Engineering', owner='Ingrid Svensson',
                 source='https://github.com/acme/analytics/pull/94', source_name='PR #94 — Export',
                 desc='CSV export for all data tables. PDF export with branded header/footer using Puppeteer. Scheduled email delivery (daily/weekly).'),
            dict(title='Permissions & Data Access Control', date='2025-03-07', status='complete',
                 cat='Engineering', owner='Ben Carter',
                 source='https://docs.google.com/document/d/analytics-permissions', source_name='Permissions Design',
                 desc='Row-level security mapped to account roles. Dashboard sharing: view-only link, org-wide, or specific users. Audit log for data access.'),
            dict(title='Beta Launch — 50 customers', date='2025-04-04', status='in-progress',
                 cat='Launch', owner='Zoe Mitchell',
                 source='https://docs.google.com/spreadsheets/d/analytics-beta-tracker', source_name='Beta Customer Tracker',
                 desc='50 enterprise customers in beta. Weekly feedback calls. Average session time: 18 minutes. NPS from beta cohort: 72.'),
            dict(title='GA Launch — Self-Serve Analytics', date='2025-06-06', status='pending',
                 cat='Launch', owner='Claire Bouchard',
                 source='https://docs.google.com/document/d/analytics-ga-plan', source_name='GA Launch Plan',
                 desc='Available on Pro and Enterprise plans. Included in Q2 pricing packaging update.'),
        ])
        self._ev(p, [
            dict(title='Theo Papadopoulos joins as Senior Data Engineer', date='2024-09-02', etype='hire',
                 people='Theo Papadopoulos', owner='Anya Sokolova',
                 desc='Theo joins from Looker with expertise in semantic layers and BI tooling.'),
            dict(title='Cube.js query timeout issues in beta', date='2025-04-18', etype='risk',
                 people='Theo Papadopoulos, Fatima Al-Hassan', owner='Theo Papadopoulos',
                 desc='Complex queries timing out for large accounts (>5M rows). Pre-aggregation strategy being expanded. Workaround: query limits with user messaging.',
                 resolved=False),
            dict(title='Pricing model decision for analytics tier', date='2025-02-21', etype='note',
                 people='Claire Bouchard, Amir Hassan, David Okonkwo', owner='Claire Bouchard',
                 desc='Analytics included in Pro plan ($49/mo) and Enterprise. No usage-based pricing in v1. Revisit after 6 months of adoption data.'),
        ])
        return p

    # =========================================================================
    # PROJECT 8 — Growth Experimentation Platform
    # =========================================================================
    def _project_growth_exp(self, owner):
        p = Project.objects.create(name='Growth Experimentation Platform', owner=owner)
        self._ms(p, [
            dict(title='Experimentation Strategy & Tooling Audit', date='2024-07-12', status='complete',
                 cat='Planning', owner='Olivia Grant',
                 source='https://docs.google.com/document/d/exp-strategy', source_name='Experimentation Strategy',
                 desc='Current state: ad-hoc feature flags in code. Target: self-serve A/B testing for Growth team. GrowthBook selected over Optimizely and LaunchDarkly.'),
            dict(title='GrowthBook Integration — Backend', date='2024-08-23', status='complete',
                 cat='Engineering', owner='Jordan Ellis',
                 source='https://github.com/acme/platform/pull/156', source_name='PR #156 — GrowthBook Backend',
                 desc='GrowthBook SDK integrated into API gateway. Feature flag evaluation: <1ms. Experiment assignment logged to CDP for analysis.'),
            dict(title='GrowthBook Integration — Frontend & Mobile', date='2024-09-20', status='complete',
                 cat='Engineering', owner='Tom Ashford',
                 source='https://github.com/acme/platform/pull/178', source_name='PR #178 — GrowthBook Frontend',
                 desc='JS and React Native SDKs integrated. Visual editor for no-code experiments. Flicker-free implementation using server-side evaluation.'),
            dict(title='Statistical Engine & Guardrail Metrics', date='2024-10-18', status='complete',
                 cat='Engineering', owner='Yara Salameh',
                 source='https://docs.google.com/document/d/stats-engine', source_name='Stats Engine Design',
                 desc='Sequential testing with SPRT for early stopping. 8 guardrail metrics defined (latency, error rate, churn). Automatic experiment pausing on guardrail breach.'),
            dict(title='Growth Team Self-Serve Launch', date='2024-11-15', status='complete',
                 cat='Launch', owner='Olivia Grant',
                 source='https://docs.google.com/document/d/growth-self-serve-launch', source_name='Self-Serve Launch Plan',
                 desc='Growth team fully self-serve for A/B tests. 8 experiments launched in first month. Experimentation velocity: from 2/quarter to 6/month.'),
            dict(title='Experiment Results Automation & Reporting', date='2025-01-10', status='complete',
                 cat='Engineering', owner='Simone Duval',
                 source='https://github.com/acme/growth-reporting/pull/12', source_name='PR #12 — Results Automation',
                 desc='Automated Slack reports on experiment completion. Results linked to CDP segments. Win/loss/inconclusive classification with plain-language summaries.'),
            dict(title='Engineering Self-Serve Access', date='2025-02-14', status='complete',
                 cat='Launch', owner='Jordan Ellis',
                 source='https://docs.google.com/document/d/eng-exp-access', source_name='Engineering Access Guide',
                 desc='All engineers can now create and manage experiments. Training completed for all 12 teams. Experiment review board established for high-risk changes.'),
            dict(title='Multi-Armed Bandit Support', date='2025-03-21', status='in-progress',
                 cat='Engineering', owner='Riku Yamamoto',
                 source='https://github.com/acme/platform/pull/289', source_name='PR #289 — MAB Support',
                 desc='Thompson sampling MAB for continuous optimisation (e.g., pricing, CTA copy). Useful for experiments where manual stopping is impractical.'),
            dict(title='Product-Wide Experimentation Playbook', date='2025-04-11', status='pending',
                 cat='Documentation', owner='Olivia Grant',
                 source='https://notion.so/acme/experimentation-playbook', source_name='Experimentation Playbook',
                 desc='Hypothesis templates, sample size calculator, common pitfalls, and 12 case studies from past experiments. Target audience: all PMs and engineers.'),
        ])
        self._ev(p, [
            dict(title='Simone Duval joins as Growth Analyst', date='2024-07-08', etype='hire',
                 people='Simone Duval', owner='Olivia Grant',
                 desc='Simone joins from Airbnb Growth with expertise in causal inference and experimentation design.'),
            dict(title='Sample Ratio Mismatch found in 3 live experiments', date='2024-12-09', etype='risk',
                 people='Yara Salameh, Simone Duval', owner='Yara Salameh',
                 desc='SRM detected in 3 experiments due to bot traffic leaking into experiment population. Bot exclusion filter added to assignment logic.',
                 resolved=True),
            dict(title='Riku Yamamoto joins as Growth Engineer', date='2025-01-06', etype='hire',
                 people='Riku Yamamoto', owner='Olivia Grant',
                 desc='Riku joins from Figma Growth. Specialises in growth infrastructure and conversion optimisation.'),
            dict(title='Experiment platform SOC 2 requirement flagged', date='2025-02-28', etype='risk',
                 people='Jordan Ellis, Priya Nair, Olivia Grant', owner='Jordan Ellis',
                 desc='Enterprise customer requires SOC 2 evidence that experiment data does not leak PII. Data anonymisation layer being added to assignment logs.',
                 resolved=False),
        ])
        return p

    # =========================================================================
    # PROJECT 9 — Enterprise SSO & Compliance
    # =========================================================================
    def _project_sso_compliance(self, owner):
        p = Project.objects.create(name='Enterprise SSO & Compliance', owner=owner)
        self._ms(p, [
            dict(title='Enterprise Auth Requirements', date='2025-01-10', status='complete',
                 cat='Planning', owner='Priya Nair',
                 source='https://docs.google.com/document/d/enterprise-auth-req', source_name='Enterprise Auth Requirements',
                 desc='Requirements gathered from 8 enterprise prospects. Must-have: SAML 2.0, SCIM provisioning, and SOC 2 Type II. Nice-to-have: OIDC, Just-in-Time provisioning.'),
            dict(title='SAML 2.0 Implementation', date='2025-02-07', status='complete',
                 cat='Engineering', owner='Jordan Ellis',
                 source='https://github.com/acme/platform/pull/267', source_name='PR #267 — SAML 2.0',
                 desc='SAML 2.0 SP implementation using python3-saml. Tested with Okta, Azure AD, OneLogin, and Google Workspace. 4 enterprise pilots onboarded.'),
            dict(title='SCIM User Provisioning', date='2025-03-07', status='complete',
                 cat='Engineering', owner='Dae-Jung Kim',
                 source='https://github.com/acme/platform/pull/298', source_name='PR #298 — SCIM',
                 desc='SCIM 2.0 provisioning and de-provisioning. Automated seat management. Tested with Okta and Azure AD provisioning agents.'),
            dict(title='SOC 2 Type II — Audit Readiness', date='2025-04-04', status='complete',
                 cat='Compliance', owner='Marcus Webb',
                 source='https://docs.google.com/spreadsheets/d/soc2-controls-tracker', source_name='SOC 2 Controls Tracker',
                 desc='86 controls mapped across security, availability, and confidentiality. Evidence collection automated for 60% of controls. Auditor: Schellman.'),
            dict(title='Audit Log & Admin Console', date='2025-04-25', status='in-progress',
                 cat='Engineering', owner='Omar Osei',
                 source='https://github.com/acme/platform/pull/334', source_name='PR #334 — Audit Log',
                 desc='Immutable audit log for all admin actions. Admin console: user management, SSO config, and session management. Export to SIEM via webhook.'),
            dict(title='SOC 2 Type II Audit', date='2025-06-13', status='pending',
                 cat='Compliance', owner='Marcus Webb',
                 source='https://docs.google.com/document/d/soc2-audit-plan', source_name='SOC 2 Audit Plan',
                 desc='Schellman conducting 6-week audit covering 12-month observation period. Report expected August 2025.'),
            dict(title='SOC 2 Report & Customer Trust Portal', date='2025-09-05', status='pending',
                 cat='Compliance', owner='Rachel Torres',
                 source='https://docs.google.com/document/d/trust-portal-plan', source_name='Trust Portal Plan',
                 desc='SOC 2 Type II report published. Trust portal (security.acme.com) with report, pen test summaries, and uptime history.'),
            dict(title='OIDC & Just-in-Time Provisioning', date='2025-10-17', status='pending',
                 cat='Engineering', owner='Priya Nair',
                 source='https://docs.google.com/document/d/oidc-jit-design', source_name='OIDC + JIT Design',
                 desc='OIDC provider support and JIT account creation for enterprise customers who prefer not to use SCIM provisioning.'),
            dict(title='Enterprise GA & Sales Enablement', date='2025-12-05', status='pending',
                 cat='Launch', owner='Rachel Torres',
                 source='https://docs.google.com/document/d/enterprise-ga-plan', source_name='Enterprise GA Plan',
                 desc='Enterprise tier generally available. Sales battle cards, competitive positioning, and demo environment updated.'),
        ])
        self._ev(p, [
            dict(title='Enterprise sales pipeline — 3 deals blocked on SSO', date='2025-01-06', etype='risk',
                 people='Amir Hassan, Rachel Torres, Marcus Webb', owner='Rachel Torres',
                 desc='3 enterprise deals ($480k ARR) stalled on lack of SSO. Project elevated to P0 priority. Timeline pulled forward by 6 weeks.',
                 resolved=True),
            dict(title='Okta partnership agreement signed', date='2025-02-14', etype='note',
                 people='Amir Hassan, Priya Nair', owner='Amir Hassan',
                 desc='Technology partner agreement with Okta. Listed in Okta Integration Network. Co-marketing agreed for Q3 2025.'),
            dict(title='SCIM provisioning data loss incident', date='2025-03-21', etype='risk',
                 people='Dae-Jung Kim, Marcus Webb', owner='Marcus Webb',
                 desc='SCIM deprovision event incorrectly deleted 3 enterprise user accounts in staging. Safeguard added: soft-delete with 7-day recovery window. Not reached production.',
                 resolved=True),
            dict(title='Schellman audit engagement confirmed', date='2025-04-14', etype='note',
                 people='Marcus Webb, Rachel Torres', owner='Marcus Webb',
                 desc='Schellman confirmed as SOC 2 auditor. Observation period: July 2024 – June 2025. Kickoff call scheduled for June 16.'),
        ])
        return p

    # =========================================================================
    # PROJECT 10 — Content & SEO Overhaul
    # =========================================================================
    def _project_content_seo(self, owner):
        p = Project.objects.create(name='Content & SEO Overhaul', owner=owner)
        self._ms(p, [
            dict(title='SEO Audit & Keyword Research', date='2025-03-07', status='complete',
                 cat='Research', owner='Tyler Rhodes',
                 source='https://docs.google.com/spreadsheets/d/seo-audit-2025', source_name='SEO Audit 2025',
                 desc='Technical SEO audit: 214 issues found across 3 severity levels. Keyword gap analysis vs 5 competitors. 120 priority keyword clusters identified.'),
            dict(title='Content Strategy & Pillar Framework', date='2025-03-28', status='complete',
                 cat='Strategy', owner='Nadia Obi',
                 source='https://docs.google.com/document/d/content-strategy-2025', source_name='Content Strategy 2025',
                 desc='6 content pillars aligned to ICP jobs-to-be-done. Hub-and-spoke model. 3 content types: pillar pages, cluster articles, and comparison pages.'),
            dict(title='Technical SEO Fixes — Phase 1', date='2025-04-18', status='complete',
                 cat='Engineering', owner='Carlos Mendes',
                 source='https://github.com/acme/website/pull/134', source_name='PR #134 — SEO Fixes',
                 desc='Core Web Vitals: LCP 1.1s, CLS 0.04, INP 180ms. Structured data added to 38 pages. Canonical tags, hreflang, and sitemap corrected.'),
            dict(title='Pillar Pages — 6 Topics', date='2025-05-16', status='in-progress',
                 cat='Content', owner='Freya Nielsen',
                 source='https://docs.google.com/spreadsheets/d/content-calendar', source_name='Content Calendar',
                 desc='6 long-form pillar pages (3,000–5,000 words each). 3 published, 3 in draft. Target: top-3 ranking for each primary keyword within 6 months.'),
            dict(title='Blog Migration & CMS Upgrade', date='2025-06-06', status='pending',
                 cat='Engineering', owner='Carlos Mendes',
                 source='https://docs.google.com/document/d/cms-migration-plan', source_name='CMS Migration Plan',
                 desc='Migrate blog from WordPress to Contentful. 180 articles to be migrated and audited. 40 articles to be consolidated or deleted.'),
            dict(title='Comparison & Alternative Pages (20 pages)', date='2025-07-11', status='pending',
                 cat='Content', owner='Tyler Rhodes',
                 source='https://docs.google.com/spreadsheets/d/comparison-pages-tracker', source_name='Comparison Pages Tracker',
                 desc='High-intent bottom-of-funnel pages targeting competitor comparison searches. Each page: 1,500 words + data table + FAQ schema.'),
            dict(title='Link Building Campaign', date='2025-08-08', status='pending',
                 cat='Marketing', owner='Pita Havili',
                 source='https://docs.google.com/spreadsheets/d/link-building-tracker', source_name='Link Building Tracker',
                 desc='Target: 40 referring domains in 90 days. Tactics: digital PR, original data studies, and podcast guest appearances.'),
            dict(title='SEO Programme Review — 6-Month Results', date='2025-09-19', status='pending',
                 cat='Review', owner='Tyler Rhodes',
                 source='https://docs.google.com/presentation/d/seo-6mo-review', source_name='SEO 6-Month Review',
                 desc='Review organic traffic growth, keyword rankings, and pipeline attribution. Adjust strategy based on results.'),
            dict(title='Content & SEO Overhaul — Phase 2 Planning', date='2025-12-05', status='pending',
                 cat='Planning', owner='Nadia Obi',
                 source='https://docs.google.com/document/d/content-phase2', source_name='Content Phase 2 Plan',
                 desc='Phase 2 scope: video content, podcast, and localisation for 3 new markets (DE, FR, ES).'),
        ])
        self._ev(p, [
            dict(title='Tyler Rhodes joins as SEO Lead', date='2025-03-03', etype='hire',
                 people='Tyler Rhodes', owner='Olivia Grant',
                 desc='Tyler joins from HubSpot SEO team. Led blog SEO strategy that grew organic traffic 3× in 2 years.'),
            dict(title='Google algorithm update — March 2025 Core Update', date='2025-03-15', etype='risk',
                 people='Tyler Rhodes, Nadia Obi', owner='Tyler Rhodes',
                 desc='Core update caused 12% traffic dip on 3 blog categories. Recovery plan: content quality improvements and E-E-A-T signals. Monitoring weekly.',
                 resolved=False),
            dict(title='Freya Nielsen joins as Content Strategist', date='2025-04-07', etype='hire',
                 people='Freya Nielsen', owner='Nadia Obi',
                 desc='Freya joins from Intercom Content team. Specialist in B2B SaaS content strategy and SEO writing.'),
            dict(title='SEO agency partnership — Distilled engaged', date='2025-04-21', etype='note',
                 people='Tyler Rhodes, Olivia Grant', owner='Olivia Grant',
                 desc='Distilled engaged for technical SEO consulting and link building support. 6-month contract.'),
        ])
        return p

    # =========================================================================
    # DASHBOARDS
    # =========================================================================
    def _seed_dashboards(self, projects):
        # Fetch project objects by their seed key
        p = lambda key: projects[key]
        jordan = self._users['jordan.ellis']
        marcus = self._users['marcus.webb']
        rachel = self._users['rachel.torres']

        # ── Dashboard A: Jordan Ellis — IC View ──────────────────────────────
        ic_dash = Dashboard.objects.create(name='Jordan Ellis — IC View', owner=jordan)
        for proj in [
            p('_project_platform_rebuild'),
            p('_project_cdp'),
            p('_project_mobile_app'),
            p('_project_growth_exp'),
        ]:
            DashboardProject.objects.create(dashboard=ic_dash, project=proj)

        # ── Dashboard B: Marcus Webb — Manager View ───────────────────────────
        mgr_dash = Dashboard.objects.create(name='Marcus Webb — Platform Engineering', owner=marcus)
        for proj in [
            p('_project_platform_rebuild'),
            p('_project_cdp'),
            p('_project_mobile_app'),
            p('_project_growth_exp'),
            p('_project_sso_compliance'),
        ]:
            DashboardProject.objects.create(dashboard=mgr_dash, project=proj)

        # ── Dashboard C: Rachel Torres — Director View ────────────────────────
        dir_dash = Dashboard.objects.create(name='Rachel Torres — Director View', owner=rachel)
        for proj in [
            p('_project_platform_rebuild'),
            p('_project_cdp'),
            p('_project_mobile_app'),
            p('_project_growth_exp'),
            p('_project_sso_compliance'),
            p('_project_design_system'),
            p('_project_ml_reco'),
            p('_project_self_serve_analytics'),
        ]:
            DashboardProject.objects.create(dashboard=dir_dash, project=proj)

        self.stdout.write(f'  ✓ Dashboard: {ic_dash.name} ({ic_dash.projects.count()} projects)')
        self.stdout.write(f'  ✓ Dashboard: {mgr_dash.name} ({mgr_dash.projects.count()} projects)')
        self.stdout.write(f'  ✓ Dashboard: {dir_dash.name} ({dir_dash.projects.count()} projects)')
