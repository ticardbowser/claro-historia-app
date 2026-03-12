from django.core.management.base import BaseCommand
from tracker.models import Project, Milestone, Event


class Command(BaseCommand):
    help = 'Seeds the database with 5 projects spanning 2 years (2024–2025)'

    def handle(self, *args, **options):
        Project.objects.all().delete()  # cascades to milestones and events
        self.stdout.write('Cleared existing data.')

        projects = [
            self._project_1,
            self._project_2,
            self._project_3,
            self._project_4,
            self._project_5,
        ]

        for fn in projects:
            fn()

        self.stdout.write(self.style.SUCCESS(
            f'Done. Seeded {Project.objects.count()} projects, '
            f'{Milestone.objects.count()} milestones, '
            f'{Event.objects.count()} events.'
        ))

    # ─────────────────────────────────────────────────────────────────────────
    # Project 1 — Website Redesign (Jan 2024 – Dec 2024, COMPLETE)
    # ─────────────────────────────────────────────────────────────────────────
    def _project_1(self):
        p = Project.objects.create(name='Website Redesign')

        milestones = [
            dict(title='Project Kickoff', date='2024-01-08', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/kickoff-brief', source_name='Kickoff Brief',
                 desc='Align all stakeholders on scope, timeline, and success metrics. 14 attendees across Product, Engineering, and Marketing.'),
            dict(title='Stakeholder Interviews', date='2024-01-22', status='complete', cat='Research',
                 source='https://docs.google.com/document/d/stakeholder-interviews', source_name='Interview Notes',
                 desc='12 interviews across 5 departments. Key themes: mobile UX, page speed, and brand refresh.'),
            dict(title='User Research & Competitive Analysis', date='2024-02-05', status='complete', cat='Research',
                 source='https://docs.google.com/presentation/d/research-findings', source_name='Research Deck',
                 desc='22 user sessions recorded. Competitive benchmarking against 6 peers completed.'),
            dict(title='Information Architecture', date='2024-02-19', status='complete', cat='Design',
                 source='https://www.figma.com/file/ia-sitemap', source_name='Figma — Sitemap',
                 desc='New sitemap reduces top-level nav from 9 to 5 items. 34% of pages flagged for consolidation.'),
            dict(title='Design System v1', date='2024-03-08', status='complete', cat='Design',
                 source='https://www.figma.com/file/design-system', source_name='Figma — Design System',
                 desc='62 components, colour tokens, typography scale, and motion principles documented.'),
            dict(title='High-Fidelity Wireframes', date='2024-03-29', status='complete', cat='Design',
                 source='https://www.figma.com/file/wireframes', source_name='Figma — Wireframes',
                 desc='All 18 page templates designed at desktop and mobile breakpoints with accessibility annotations.'),
            dict(title='Stakeholder Design Sign-off', date='2024-04-05', status='complete', cat='Review',
                 source='https://docs.google.com/presentation/d/design-review', source_name='Design Review Deck',
                 desc='CMO and CPO signed off. 7 revision requests raised; 5 resolved same day.'),
            dict(title='Frontend Build — Marketing Pages', date='2024-05-10', status='complete', cat='Engineering',
                 source='https://github.com/org/website/pull/54', source_name='PR #54',
                 desc='Home, About, Pricing, Contact built. Lighthouse: Performance 94, Accessibility 98, SEO 100.'),
            dict(title='CMS Integration (Contentful)', date='2024-05-24', status='complete', cat='Engineering',
                 source='https://docs.google.com/document/d/cms-spec', source_name='CMS Spec',
                 desc='Blog, changelog, and docs connected to Contentful. 12 articles migrated.'),
            dict(title='Frontend Build — Product Pages', date='2024-06-14', status='complete', cat='Engineering',
                 source='https://github.com/org/website/pull/89', source_name='PR #89',
                 desc='Dashboard shell, onboarding flow, and settings pages built. Auth integration complete.'),
            dict(title='Internal QA Round 1', date='2024-06-28', status='complete', cat='QA',
                 source='https://docs.google.com/spreadsheets/d/qa-round-1', source_name='QA Tracker Round 1',
                 desc='48 issues logged. 2 P0s resolved in 48 hours. All P1s cleared within the sprint.'),
            dict(title='Performance & SEO Optimisation', date='2024-07-12', status='complete', cat='Engineering',
                 source='https://docs.google.com/document/d/perf-report', source_name='Perf & SEO Report',
                 desc='LCP improved from 3.8s to 1.2s. Structured data added to all product pages.'),
            dict(title='Accessibility Audit (WCAG 2.1 AA)', date='2024-07-26', status='complete', cat='QA',
                 source='https://docs.google.com/document/d/a11y-audit', source_name='Accessibility Audit',
                 desc='Third-party audit by Deque. 14 issues found and resolved. Certified WCAG 2.1 AA.'),
            dict(title='Stakeholder UAT Sign-off', date='2024-08-09', status='complete', cat='Review',
                 source='https://docs.google.com/spreadsheets/d/uat-sign-off', source_name='UAT Sign-off',
                 desc='8 stakeholders tested against all acceptance criteria. CPO and CTO gave final green light.'),
            dict(title='Soft Launch — Beta Users', date='2024-08-30', status='complete', cat='Launch',
                 source='https://docs.google.com/document/d/soft-launch', source_name='Soft Launch Report',
                 desc='Opened to 500 beta users. 99.98% uptime over first 72 hours. 23 UX issues triaged.'),
            dict(title='Public Launch', date='2024-09-04', status='complete', cat='Launch',
                 source='https://docs.google.com/presentation/d/launch-deck', source_name='Launch Deck',
                 desc='#3 Product Hunt on launch day. 18,400 unique visitors in 24 hours. Zero downtime.'),
            dict(title='Post-launch Analytics Review', date='2024-09-20', status='complete', cat='Research',
                 source='https://docs.google.com/presentation/d/post-launch', source_name='Post-launch Analytics',
                 desc='Bounce rate down 31%. Session duration up to 3m 08s. Conversion rate up 18%.'),
            dict(title='Localisation — French & German', date='2024-11-15', status='complete', cat='Engineering',
                 source='https://github.com/org/website/pull/201', source_name='PR #201 — i18n',
                 desc='next-intl integrated. French and German locales launched on schedule.'),
            dict(title='A/B Test — Pricing Page', date='2024-12-06', status='complete', cat='Growth',
                 source='https://docs.google.com/document/d/ab-test-pricing', source_name='A/B Test Results',
                 desc='Variant B (value-prop-first) shipped at 97% confidence. +11% trial sign-up rate.'),
            dict(title='Year-end Handover to Web Team', date='2024-12-20', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/handover', source_name='Handover Doc',
                 desc='Full ownership transferred. All runbooks, credentials, and documentation handed over.'),
        ]
        for m in milestones:
            Milestone.objects.create(project=p, **m)

        events = [
            dict(title='Sarah Chen joins as Lead Designer', date='2024-01-06', etype='hire', people='Sarah Chen',
                 source='https://docs.google.com/document/d/offer-sarah', source_name='Offer Letter',
                 desc='Sarah brings 8 years of experience from Figma and Shopify. Leads visual design and the design system.'),
            dict(title='Marcus Webb departs the project', date='2024-01-24', etype='depart', people='Marcus Webb',
                 source='https://mail.google.com/mail/u/0/#inbox/marcus-offboarding', source_name='Offboarding Thread',
                 desc='Marcus moved to a new internal Platform role. Frontend work redistributed to Priya Nair and Dev Kapoor.'),
            dict(title='Priya Nair joins as Frontend Engineer', date='2024-02-03', etype='hire', people='Priya Nair',
                 desc='Priya joins to backfill frontend capacity. Specialises in React performance and accessibility.'),
            dict(title='Design team restructured under Engineering', date='2024-02-09', etype='reorg',
                 people='Sarah Chen, Priya Nair, Dev Kapoor',
                 source='https://docs.google.com/document/d/reorg-feb24', source_name='Reorg Memo',
                 desc='Design and engineering merged into a single cross-functional pod. Weekly design-dev syncs introduced.'),
            dict(title='Switched from Webpack to Vite', date='2024-02-14', etype='tech',
                 source='https://docs.google.com/spreadsheets/d/build-benchmarks', source_name='Build Benchmarks',
                 desc='Build times reduced from 42s to 4s. HMR now 180ms. CI pipeline updated.'),
            dict(title='Mapping API rate limit risk flagged', date='2024-02-23', etype='risk', people='Dev Kapoor',
                 source='https://docs.google.com/document/d/api-risk', source_name='API Risk Assessment',
                 desc='Contact page mapping API has a 500 req/day free tier cap. Upgrade or caching required before launch.'),
            dict(title='Jordan Kim joins as QA Engineer', date='2024-03-04', etype='hire', people='Jordan Kim',
                 desc='Jordan joins for the build and pre-launch phase. Owns QA tracker and Playwright E2E suite.'),
            dict(title='Contentful CMS selected over Sanity', date='2024-04-03', etype='tech',
                 people='Dev Kapoor, Alejandro Reyes',
                 source='https://docs.google.com/document/d/cms-evaluation', source_name='CMS Evaluation',
                 desc='Contentful selected after evaluating 3 options. Signed for editorial UX and webhook support.'),
            dict(title='Scope change: Docs hub added to Phase 1', date='2024-04-15', etype='risk',
                 people='CPO, Dev Kapoor',
                 source='https://docs.google.com/document/d/scope-change', source_name='Scope Change Request',
                 desc='CPO added full docs hub to September launch scope. Adds ~3 weeks engineering. Confirmed feasible.'),
            dict(title='Dev Kapoor promoted to Tech Lead', date='2024-05-06', etype='reorg', people='Dev Kapoor',
                 desc='Dev takes technical leadership, conducting code reviews and owning architecture decisions.'),
            dict(title='GDPR cookie compliance flagged by Legal', date='2024-06-10', etype='risk',
                 people='Legal, Dev Kapoor',
                 source='https://docs.google.com/document/d/gdpr-review', source_name='GDPR Review',
                 desc='EU consent banners required. OneTrust integrated and tested. Legal sign-off received June 23.'),
            dict(title='Jordan Kim departs — contract end', date='2024-06-21', etype='depart', people='Jordan Kim',
                 desc='4-month QA contract concluded. Playwright suite covers 94% of critical user flows.'),
            dict(title='Aisha Okonkwo joins as Growth Engineer', date='2024-07-29', etype='hire',
                 people='Aisha Okonkwo',
                 desc='Aisha owns post-launch A/B testing (LaunchDarkly) and conversion optimisation.'),
            dict(title='External pen test — medium finding patched', date='2024-07-19', etype='risk',
                 people='Dev Kapoor',
                 source='https://docs.google.com/document/d/pentest-report', source_name='Pen Test Report',
                 desc='Insufficiently scoped CORS policy patched same day. 3 low findings resolved in 48 hours.'),
            dict(title='Public launch — site live', date='2024-09-04', etype='note', people='Full team',
                 desc='Zero downtime deploy at 09:00 UTC. Product Hunt #3. 18,400 unique visitors day one.'),
            dict(title='Post-launch iOS 16 nav bug hotfixed', date='2024-09-05', etype='risk', people='Priya Nair',
                 source='https://github.com/org/website/issues/234', source_name='GitHub Issue #234',
                 desc='CSS scroll-lock froze mobile nav on iOS 16 Safari. Hotfix live within 4 hours. ~8% of traffic affected.'),
            dict(title='Next.js upgraded to v15', date='2024-10-14', etype='tech', people='Dev Kapoor, Priya Nair',
                 source='https://github.com/org/website/pull/189', source_name='PR #189',
                 desc='App Router fully adopted. Partial Prerendering on marketing pages. Build time down 22%.'),
            dict(title='Priya Nair promoted to Senior Frontend Engineer', date='2024-11-18', etype='reorg',
                 people='Priya Nair',
                 desc='Promoted after exceptional performance. Takes on mentoring responsibilities for 2 junior engineers in 2025.'),
            dict(title='2025 web roadmap approved by leadership', date='2024-12-09', etype='note',
                 people='Dev Kapoor, Aisha Okonkwo',
                 source='https://docs.google.com/presentation/d/2025-roadmap', source_name='2025 Roadmap Deck',
                 desc='Roadmap covering video integration, personalisation engine, and expanded localisation approved. Budget confirmed.'),
        ]
        for e in events:
            Event.objects.create(project=p, **e)

        self.stdout.write(f'  ✓ {p.name} — {len(milestones)} milestones, {len(events)} events')

    # ─────────────────────────────────────────────────────────────────────────
    # Project 2 — Mobile App Launch (Mar 2024 – Aug 2025, IN PROGRESS)
    # ─────────────────────────────────────────────────────────────────────────
    def _project_2(self):
        p = Project.objects.create(name='Mobile App Launch')

        milestones = [
            dict(title='Product Vision & OKRs', date='2024-03-11', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/mobile-vision', source_name='Vision Doc',
                 desc='Product vision, OKRs, and success metrics defined. North star: 100k MAU within 6 months of launch.'),
            dict(title='Technical Architecture Decision', date='2024-03-25', status='complete', cat='Engineering',
                 source='https://docs.google.com/document/d/tech-arch', source_name='Architecture Doc',
                 desc='React Native selected over Flutter. Monorepo with shared business logic between iOS and Android.'),
            dict(title='UX Research — Mobile Habits', date='2024-04-08', status='complete', cat='Research',
                 source='https://docs.google.com/presentation/d/mobile-research', source_name='UX Research Deck',
                 desc='Diary studies with 30 participants over 2 weeks. Key insight: 73% of target users access product during commute.'),
            dict(title='App Design System', date='2024-04-26', status='complete', cat='Design',
                 source='https://www.figma.com/file/app-design-system', source_name='Figma — App Design System',
                 desc='Native-first component library. iOS and Android variants for all 48 components. Dark mode included.'),
            dict(title='Core Feature Wireframes — v1', date='2024-05-17', status='complete', cat='Design',
                 source='https://www.figma.com/file/app-wireframes', source_name='Figma — App Wireframes',
                 desc='Onboarding, home feed, profile, notifications, and settings screens completed.'),
            dict(title='Backend API v1 — Auth & Core', date='2024-06-07', status='complete', cat='Engineering',
                 source='https://github.com/org/mobile-api/pull/12', source_name='PR #12 — API v1',
                 desc='Authentication, user profiles, and core data endpoints live on staging. 98% test coverage.'),
            dict(title='iOS Alpha Build', date='2024-07-05', status='complete', cat='Engineering',
                 source='https://github.com/org/mobile-app/releases/alpha-1', source_name='Alpha Release Notes',
                 desc='First testable iOS build distributed via TestFlight to 25 internal testers.'),
            dict(title='Android Alpha Build', date='2024-07-19', status='complete', cat='Engineering',
                 source='https://github.com/org/mobile-app/releases/android-alpha', source_name='Android Alpha Notes',
                 desc='Android alpha distributed via Firebase App Distribution to 20 internal testers.'),
            dict(title='Internal Alpha Testing & Bug Bash', date='2024-08-02', status='complete', cat='QA',
                 source='https://docs.google.com/spreadsheets/d/alpha-bugs', source_name='Alpha Bug Tracker',
                 desc='Bug bash with 45 employees. 112 issues logged. All P0/P1s resolved in 2-week sprint.'),
            dict(title='Beta Programme Launch', date='2024-09-06', status='complete', cat='Launch',
                 source='https://docs.google.com/document/d/beta-programme', source_name='Beta Programme Brief',
                 desc='2,000 beta users recruited via waitlist. NPS after 2 weeks: 61.'),
            dict(title='Push Notifications & Deep Links', date='2024-09-27', status='complete', cat='Engineering',
                 source='https://github.com/org/mobile-app/pull/78', source_name='PR #78',
                 desc='FCM and APNs integrated. Deep link routing for all 14 core screens. A/B tested onboarding push sequence.'),
            dict(title='App Store & Play Store Assets', date='2024-10-18', status='complete', cat='Marketing',
                 source='https://www.figma.com/file/store-assets', source_name='Figma — Store Assets',
                 desc='Screenshots, feature graphic, preview video, and app description copy finalised for both stores.'),
            dict(title='App Store Review Submission', date='2024-11-01', status='complete', cat='Launch',
                 source='https://docs.google.com/document/d/app-store-submission', source_name='Submission Checklist',
                 desc='Submitted to Apple App Store and Google Play. First Apple review rejected (minor metadata issue); resubmitted Nov 4.'),
            dict(title='Public Launch — iOS & Android', date='2024-11-15', status='complete', cat='Launch',
                 source='https://docs.google.com/presentation/d/mobile-launch-deck', source_name='Launch Deck',
                 desc='Simultaneous launch on both stores. 8,200 downloads on day one. Featured in App Store "New Apps We Love".'),
            dict(title='Post-launch Crash Rate < 0.5%', date='2024-12-06', status='complete', cat='Engineering',
                 source='https://docs.google.com/spreadsheets/d/crash-report-dec', source_name='Crash Report',
                 desc='Crash-free session rate stabilised at 99.6%. Top 3 crash causes resolved via hotfix releases.'),
            dict(title='v1.1 — Offline Mode', date='2025-01-17', status='complete', cat='Engineering',
                 source='https://github.com/org/mobile-app/pull/134', source_name='PR #134 — Offline',
                 desc='Full offline read access with background sync. Most-requested feature from beta feedback. 4.6★ average after release.'),
            dict(title='v1.2 — Collaborative Features', date='2025-03-07', status='complete', cat='Engineering',
                 source='https://github.com/org/mobile-app/pull/167', source_name='PR #167 — Collab',
                 desc='Shared workspaces, real-time presence, and in-app commenting shipped. DAU up 34% week-over-week.'),
            dict(title='50k MAU Milestone', date='2025-04-01', status='complete', cat='Growth',
                 desc='Reached 50,000 monthly active users — halfway to North Star goal ahead of schedule.'),
            dict(title='v1.3 — Widgets & Lock Screen', date='2025-05-16', status='complete', cat='Engineering',
                 source='https://github.com/org/mobile-app/pull/198', source_name='PR #198 — Widgets',
                 desc='iOS 17 interactive widgets and lock screen integration. Android home screen widgets shipped simultaneously.'),
            dict(title='100k MAU North Star Goal', date='2025-07-01', status='in-progress', cat='Growth',
                 desc='Tracking toward 100k MAU target. Currently at 78k. Paid UA campaign running June–July.'),
            dict(title='v2.0 — AI-Powered Suggestions', date='2025-08-22', status='pending', cat='Engineering',
                 source='https://docs.google.com/document/d/v2-spec', source_name='v2.0 Product Spec',
                 desc='On-device ML model for personalised content suggestions. Privacy-preserving; no data leaves device.'),
        ]
        for m in milestones:
            Milestone.objects.create(project=p, **m)

        events = [
            dict(title='Lena Park joins as iOS Engineer', date='2024-03-18', etype='hire', people='Lena Park',
                 desc='Lena brings 6 years of native iOS development. Previously at Duolingo. Joins as the first mobile hire.'),
            dict(title='React Native chosen over Flutter', date='2024-03-25', etype='tech',
                 people='Dev Kapoor, Lena Park',
                 source='https://docs.google.com/document/d/rn-vs-flutter', source_name='Framework Evaluation',
                 desc='After 2-week evaluation, React Native selected for code sharing with web team and stronger hiring pool.'),
            dict(title='Omar Hassan joins as Android Engineer', date='2024-04-15', etype='hire', people='Omar Hassan',
                 desc='Omar joins to lead the Android track. Previously at Spotify. Expert in Kotlin and Jetpack Compose.'),
            dict(title='Backend API team expanded', date='2024-05-06', etype='reorg',
                 people='Dev Kapoor, Yuki Tanaka',
                 desc='Yuki Tanaka seconded from Platform team to accelerate mobile API development for Q3 alpha target.'),
            dict(title='App Store Connect account suspended — resolved', date='2024-10-07', etype='risk',
                 people='Lena Park',
                 source='https://docs.google.com/document/d/app-store-suspension', source_name='Incident Report',
                 desc='Apple suspended developer account due to billing issue. Resolved within 6 hours. No timeline impact.'),
            dict(title='Public launch — iOS & Android', date='2024-11-15', etype='note', people='Full team',
                 desc='Featured in App Store "New Apps We Love". 8,200 downloads day one. Press coverage in TechCrunch and The Verge.'),
            dict(title='Lena Park promoted to Mobile Lead', date='2025-01-13', etype='reorg', people='Lena Park',
                 desc='Lena takes overall technical leadership of the mobile team following strong delivery track record.'),
            dict(title='Third-party analytics SDK privacy risk', date='2025-02-10', etype='risk',
                 people='Omar Hassan',
                 source='https://docs.google.com/document/d/sdk-privacy-risk', source_name='SDK Privacy Audit',
                 desc='Mixpanel SDK flagged in App Store privacy audit for data collection practices. Replaced with in-house event pipeline by Feb 28.'),
            dict(title='Zara Ahmed joins as Growth PM', date='2025-03-03', etype='hire', people='Zara Ahmed',
                 desc='Zara joins to own the 100k MAU growth initiative, UA strategy, and referral programme design.'),
            dict(title='Referral programme launched', date='2025-04-14', etype='note', people='Zara Ahmed',
                 source='https://docs.google.com/document/d/referral-programme', source_name='Referral Programme Brief',
                 desc='In-app referral flow launched. 12% of new installs attributed to referrals within first 30 days.'),
            dict(title='Paid UA campaign started — Google & Meta', date='2025-06-02', etype='note',
                 people='Zara Ahmed',
                 source='https://docs.google.com/spreadsheets/d/ua-campaign-tracker', source_name='UA Campaign Tracker',
                 desc='$80k UA budget across Google UAC and Meta App Install campaigns. Target CPI: $1.20. Early CPI: $0.94.'),
            dict(title='Omar Hassan departs for new role', date='2025-06-20', etype='depart', people='Omar Hassan',
                 desc='Omar leaves for a Staff Engineer role at a Series C startup. Android responsibilities transitioned to new hire starting July.'),
        ]
        for e in events:
            Event.objects.create(project=p, **e)

        self.stdout.write(f'  ✓ {p.name} — {len(milestones)} milestones, {len(events)} events')

    # ─────────────────────────────────────────────────────────────────────────
    # Project 3 — Data Platform Migration (Jun 2024 – Jun 2025, COMPLETE)
    # ─────────────────────────────────────────────────────────────────────────
    def _project_3(self):
        p = Project.objects.create(name='Data Platform Migration')

        milestones = [
            dict(title='Current State Audit', date='2024-06-10', status='complete', cat='Research',
                 source='https://docs.google.com/document/d/data-audit', source_name='Data Audit Report',
                 desc='Full audit of legacy Redshift warehouse. 4.2TB of data, 840 tables, 120 active dashboards across 6 teams.'),
            dict(title='Target Architecture Design', date='2024-06-28', status='complete', cat='Engineering',
                 source='https://docs.google.com/document/d/target-arch', source_name='Target Architecture',
                 desc='Snowflake + dbt + Airbyte stack selected. ELT over ETL. Medallion architecture (bronze/silver/gold layers).'),
            dict(title='Vendor Contracts Signed', date='2024-07-12', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/vendor-contracts', source_name='Contract Summary',
                 desc='Snowflake Business Critical and Airbyte Cloud contracts executed. 3-year Snowflake deal with 20% discount.'),
            dict(title='Airbyte Connectors — Source Systems', date='2024-08-02', status='complete', cat='Engineering',
                 source='https://github.com/org/data-platform/pull/14', source_name='PR #14 — Connectors',
                 desc='15 source connectors configured: Postgres, Salesforce, Stripe, Hubspot, Zendesk, and 10 others. Sync schedules set.'),
            dict(title='dbt Project Scaffold & Standards', date='2024-08-23', status='complete', cat='Engineering',
                 source='https://github.com/org/data-platform/pull/28', source_name='PR #28 — dbt Scaffold',
                 desc='dbt project structure, naming conventions, testing standards, and documentation templates established.'),
            dict(title='Bronze Layer — Raw Ingestion Complete', date='2024-09-13', status='complete', cat='Engineering',
                 source='https://github.com/org/data-platform/pull/45', source_name='PR #45 — Bronze',
                 desc='All 15 sources landing in Snowflake bronze layer. Data freshness SLA: 15 minutes for critical sources.'),
            dict(title='Silver Layer — Core Transformations', date='2024-10-04', status='complete', cat='Engineering',
                 source='https://github.com/org/data-platform/pull/67', source_name='PR #67 — Silver',
                 desc='Customer, revenue, and product usage models built. 95% dbt test coverage. CI runs on every PR.'),
            dict(title='Gold Layer — Business-Facing Marts', date='2024-10-25', status='complete', cat='Engineering',
                 source='https://github.com/org/data-platform/pull/89', source_name='PR #89 — Gold',
                 desc='Marketing, Finance, and Product marts complete. All 120 legacy dashboards mapped to new models.'),
            dict(title='Looker Migration — Phase 1 (Finance)', date='2024-11-15', status='complete', cat='Analytics',
                 source='https://docs.google.com/spreadsheets/d/looker-migration', source_name='Looker Migration Tracker',
                 desc='All 34 Finance dashboards migrated to new Snowflake connection. Finance team signed off Nov 19.'),
            dict(title='Looker Migration — Phase 2 (Marketing)', date='2024-12-06', status='complete', cat='Analytics',
                 source='https://docs.google.com/spreadsheets/d/looker-migration', source_name='Looker Migration Tracker',
                 desc='42 Marketing dashboards migrated. UTM attribution model rebuilt. Marketing team signed off Dec 10.'),
            dict(title='Looker Migration — Phase 3 (Product)', date='2025-01-10', status='complete', cat='Analytics',
                 source='https://docs.google.com/spreadsheets/d/looker-migration', source_name='Looker Migration Tracker',
                 desc='44 Product dashboards migrated including funnel, retention, and feature adoption views.'),
            dict(title='Legacy Redshift Decommission', date='2025-02-07', status='complete', cat='Engineering',
                 source='https://docs.google.com/document/d/redshift-decommission', source_name='Decommission Plan',
                 desc='Redshift cluster terminated. Final backup archived to S3 Glacier. Annual cost saving: $148k.'),
            dict(title='Data Governance Framework', date='2025-03-07', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/data-governance', source_name='Data Governance Framework',
                 desc='Data catalogue (Atlan), ownership model, PII tagging policy, and access request workflow published.'),
            dict(title='Self-serve Analytics Training', date='2025-04-04', status='complete', cat='Research',
                 source='https://docs.google.com/presentation/d/training-deck', source_name='Training Deck',
                 desc='6 training sessions across 4 departments. 85 employees trained on Snowflake + Looker. Recorded sessions published.'),
            dict(title='Real-time Streaming Layer (Kafka)', date='2025-05-09', status='complete', cat='Engineering',
                 source='https://github.com/org/data-platform/pull/145', source_name='PR #145 — Kafka',
                 desc='Confluent Cloud Kafka integrated for real-time event streaming. Latency: <2s for product events. Used by 3 live dashboards.'),
            dict(title='Platform Handover to Data Engineering Team', date='2025-06-06', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/platform-handover', source_name='Handover Document',
                 desc='Full ownership transferred to permanent Data Engineering team. Runbooks, on-call playbooks, and vendor contacts handed over.'),
        ]
        for m in milestones:
            Milestone.objects.create(project=p, **m)

        events = [
            dict(title='Fatima Al-Hassan joins as Data Architect', date='2024-06-03', etype='hire',
                 people='Fatima Al-Hassan',
                 desc='Fatima leads the technical architecture. Previously designed data platforms at Stripe and Airbnb.'),
            dict(title='Snowflake selected over BigQuery and Databricks', date='2024-06-28', etype='tech',
                 people='Fatima Al-Hassan',
                 source='https://docs.google.com/document/d/warehouse-eval', source_name='Warehouse Evaluation',
                 desc='Snowflake selected after 4-week POC. Key differentiators: data sharing, virtual warehouses, and existing team familiarity.'),
            dict(title='Kai Nomura joins as Analytics Engineer', date='2024-07-08', etype='hire', people='Kai Nomura',
                 desc='Kai joins to build and maintain the dbt transformation layer. Expert in dimensional modelling and data testing.'),
            dict(title='Finance data discrepancy — resolved', date='2024-11-20', etype='risk',
                 people='Kai Nomura, Finance',
                 source='https://docs.google.com/document/d/finance-discrepancy', source_name='Incident Report',
                 desc='ARR figures in new Looker dashboard diverged from legacy by 2.3%. Root cause: timezone handling in revenue model. Fixed and retested Nov 22.'),
            dict(title='Redshift query costs spike flagged', date='2024-12-02', etype='risk', people='Fatima Al-Hassan',
                 desc='Legacy Redshift cluster showing unexpected cost spike ($12k over budget) due to migration-period dual running. Redshift sunset date brought forward to Feb.'),
            dict(title='Airbyte connector failure — Salesforce sync gap', date='2025-01-14', etype='risk',
                 people='Kai Nomura',
                 source='https://github.com/org/data-platform/issues/112', source_name='GitHub Issue #112',
                 desc='Salesforce connector failed silently for 18 hours. 3 dashboards showed stale data. Alerting improved; Slack notifications added to all sync jobs.'),
            dict(title='Data governance policy approved by leadership', date='2025-03-07', etype='note',
                 people='Fatima Al-Hassan',
                 desc='Data governance framework ratified by CTO and General Counsel. PII tagging retroactively applied to 840 tables.'),
            dict(title='Kafka real-time streaming goes live', date='2025-05-09', etype='tech',
                 people='Fatima Al-Hassan, Kai Nomura',
                 desc='First real-time dashboard (live product funnel) deployed using Kafka → Snowflake pipeline. Sub-2s latency confirmed.'),
            dict(title='Fatima Al-Hassan transitions to fractional advisory', date='2025-06-02', etype='reorg',
                 people='Fatima Al-Hassan',
                 desc='Project concluding; Fatima moves to 1 day/week advisory. Full platform owned by Kai Nomura and the Data Engineering team.'),
        ]
        for e in events:
            Event.objects.create(project=p, **e)

        self.stdout.write(f'  ✓ {p.name} — {len(milestones)} milestones, {len(events)} events')

    # ─────────────────────────────────────────────────────────────────────────
    # Project 4 — Brand Refresh (Sep 2024 – Mar 2025, COMPLETE)
    # ─────────────────────────────────────────────────────────────────────────
    def _project_4(self):
        p = Project.objects.create(name='Brand Refresh')

        milestones = [
            dict(title='Brand Audit & Competitive Landscape', date='2024-09-09', status='complete', cat='Research',
                 source='https://docs.google.com/presentation/d/brand-audit', source_name='Brand Audit Deck',
                 desc='Audit of existing brand assets, customer perception survey (n=400), and competitive identity analysis across 12 peers.'),
            dict(title='Brand Strategy Workshop', date='2024-09-27', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/brand-strategy', source_name='Brand Strategy',
                 desc='Full-day workshop with exec team and agency. Defined brand pillars: Clarity, Momentum, Trust. Positioning statement finalised.'),
            dict(title='Logo Concepts — Round 1', date='2024-10-11', status='complete', cat='Design',
                 source='https://www.figma.com/file/logo-concepts-r1', source_name='Figma — Logo R1',
                 desc='Agency presented 4 logo directions. Two advanced to Round 2: "Wordmark Evolved" and "Geometric Mark + Wordmark".'),
            dict(title='Logo Concepts — Round 2 & Selection', date='2024-10-25', status='complete', cat='Design',
                 source='https://www.figma.com/file/logo-concepts-r2', source_name='Figma — Logo R2',
                 desc='"Geometric Mark + Wordmark" selected by exec vote. Refinements completed. Trademark search initiated.'),
            dict(title='Colour Palette & Typography System', date='2024-11-08', status='complete', cat='Design',
                 source='https://www.figma.com/file/brand-tokens', source_name='Figma — Brand Tokens',
                 desc='New primary palette: deep teal (#0D5C63), warm off-white (#F5F0E8), and amber accent (#E8A246). Syne + Inconsolata retained.'),
            dict(title='Brand Guidelines Document v1', date='2024-11-22', status='complete', cat='Design',
                 source='https://www.figma.com/file/brand-guidelines', source_name='Brand Guidelines',
                 desc='72-page brand guidelines covering logo usage, colour, typography, photography, illustration, and motion principles.'),
            dict(title='Trademark Registration Filed', date='2024-12-06', status='complete', cat='Legal',
                 source='https://docs.google.com/document/d/trademark-filing', source_name='Trademark Filing',
                 desc='Wordmark and geometric mark filed with USPTO (Class 42) and EUIPO. Expected registration timeline: 12–18 months.'),
            dict(title='Internal Asset Rollout', date='2024-12-20', status='complete', cat='Launch',
                 source='https://docs.google.com/document/d/asset-rollout', source_name='Asset Rollout Plan',
                 desc='New brand applied to: email templates, slide decks, letterhead, Zoom backgrounds, and internal wikis. 340 assets updated.'),
            dict(title='Digital Properties Update', date='2025-01-17', status='complete', cat='Engineering',
                 source='https://github.com/org/brand-rollout/pull/22', source_name='PR #22 — Brand Tokens',
                 desc='Design tokens updated across website, app, and marketing emails. Dark mode and light mode variants verified.'),
            dict(title='Social Media & Marketing Channels', date='2025-01-31', status='complete', cat='Marketing',
                 source='https://docs.google.com/document/d/social-rollout', source_name='Social Rollout Plan',
                 desc='All social profiles (LinkedIn, Twitter/X, YouTube, Instagram) updated with new logo, cover images, and bios.'),
            dict(title='External Launch — Press & Announcement', date='2025-02-12', status='complete', cat='Launch',
                 source='https://docs.google.com/document/d/brand-launch-announcement', source_name='Launch Announcement',
                 desc='Brand refresh announced via blog post and press release. Coverage in Fast Company and Campaign. Positive community reception.'),
            dict(title='Swag & Physical Collateral', date='2025-02-28', status='complete', cat='Marketing',
                 source='https://docs.google.com/spreadsheets/d/swag-order', source_name='Swag Order Sheet',
                 desc='New brand applied to: t-shirts, hoodies, tote bags, stickers, and conference booth materials. 500-unit run completed.'),
            dict(title='Brand Adoption Review', date='2025-03-14', status='complete', cat='Review',
                 source='https://docs.google.com/presentation/d/brand-adoption-review', source_name='Brand Adoption Review',
                 desc='4-week post-launch survey: 91% internal satisfaction. Customer recall test showed 22% improvement vs old brand. Project closed.'),
        ]
        for m in milestones:
            Milestone.objects.create(project=p, **m)

        events = [
            dict(title='Brand agency (Monogram Studio) contracted', date='2024-09-02', etype='note',
                 people='CMO',
                 source='https://docs.google.com/document/d/agency-contract', source_name='Agency Contract',
                 desc='Monogram Studio engaged after competitive pitch process. 3-month contract for strategy through brand guidelines.'),
            dict(title='Isabel Ferreira joins as Brand Designer', date='2024-09-16', etype='hire',
                 people='Isabel Ferreira',
                 desc='Isabel joins in-house to partner with Monogram Studio and own the internal asset rollout phase.'),
            dict(title='Legal flags potential trademark conflict', date='2024-10-28', etype='risk',
                 people='Legal, CMO',
                 source='https://docs.google.com/document/d/trademark-risk', source_name='Trademark Risk Memo',
                 desc='Preliminary search found a similar geometric mark in Class 35 (advertising). Counsel advised proceeding with Class 42 filing; Class 35 conflict assessed as low risk.'),
            dict(title='CEO requests logo direction change', date='2024-11-04', etype='risk',
                 people='CEO, CMO, Isabel Ferreira',
                 desc='After seeing R2 concepts, CEO requested revisiting the "Wordmark Evolved" direction. Two-week delay absorbed into schedule. Final decision confirmed Nov 8 in favour of original recommendation.'),
            dict(title='Monogram Studio contract extended', date='2024-11-15', etype='note', people='CMO',
                 desc='Agency contract extended by 4 weeks to cover brand guidelines finalisation and launch support. Budget impact: +$18k.'),
            dict(title='Brand guidelines published internally', date='2024-11-22', etype='note',
                 people='Isabel Ferreira',
                 desc='Brand guidelines Figma file shared company-wide. Confluence page with quick-reference guide published. Slack #brand-refresh channel opened.'),
            dict(title='External brand launch', date='2025-02-12', etype='note', people='CMO, Isabel Ferreira',
                 desc='Announcement live. Blog post reached 4,200 unique views in 24 hours. Fast Company covered the story. LinkedIn post: 1,800 reactions.'),
            dict(title='Isabel Ferreira transitions to full-time Brand Lead', date='2025-03-03', etype='reorg',
                 people='Isabel Ferreira',
                 desc='Isabel converts from project-based contract to permanent Brand Lead role. Will own brand governance and evolution going forward.'),
        ]
        for e in events:
            Event.objects.create(project=p, **e)

        self.stdout.write(f'  ✓ {p.name} — {len(milestones)} milestones, {len(events)} events')

    # ─────────────────────────────────────────────────────────────────────────
    # Project 5 — AI Features Programme (Jan 2025 – Dec 2025, IN PROGRESS)
    # ─────────────────────────────────────────────────────────────────────────
    def _project_5(self):
        p = Project.objects.create(name='AI Features Programme')

        milestones = [
            dict(title='AI Strategy & Opportunity Mapping', date='2025-01-10', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/ai-strategy', source_name='AI Strategy Doc',
                 desc='Identified 12 AI feature opportunities across product surface. Scored by user value, feasibility, and strategic fit. Top 4 prioritised for 2025.'),
            dict(title='LLM Vendor Evaluation', date='2025-01-24', status='complete', cat='Research',
                 source='https://docs.google.com/document/d/llm-eval', source_name='LLM Evaluation Report',
                 desc='Evaluated OpenAI GPT-4o, Anthropic Claude, and Google Gemini on accuracy, latency, cost, and data privacy terms. Claude selected for primary use; OpenAI retained for embeddings.'),
            dict(title='AI Ethics & Safety Review', date='2025-02-07', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/ai-ethics', source_name='AI Ethics Framework',
                 desc='Internal AI ethics committee review completed. Bias testing protocol, human-in-the-loop requirements, and user transparency guidelines established.'),
            dict(title='Infrastructure: LLM Gateway & Caching Layer', date='2025-02-21', status='complete',
                 cat='Engineering',
                 source='https://github.com/org/ai-platform/pull/8', source_name='PR #8 — LLM Gateway',
                 desc='Centralised LLM gateway with request routing, semantic caching (60% cache hit rate), rate limiting, and cost tracking. Reduces LLM spend by est. 40%.'),
            dict(title='Feature 1: Smart Summarisation — Beta', date='2025-03-14', status='complete', cat='Engineering',
                 source='https://github.com/org/ai-platform/pull/23', source_name='PR #23 — Summarisation',
                 desc='AI-powered document and thread summarisation. Beta released to 500 users. Average time saved: 8 min/day per user.'),
            dict(title='Feature 1: Smart Summarisation — GA', date='2025-04-04', status='complete', cat='Engineering',
                 source='https://github.com/org/ai-platform/pull/41', source_name='PR #41 — Summarisation GA',
                 desc='General availability to all users. Opt-in rate: 68%. NPS impact: +7 points vs non-users. One-click summary in 3 surfaces.'),
            dict(title='Feature 2: AI Writing Assistant — Beta', date='2025-04-25', status='complete', cat='Engineering',
                 source='https://github.com/org/ai-platform/pull/56', source_name='PR #56 — Writing Assistant',
                 desc='In-context writing suggestions, tone adjustment, and grammar correction. Beta: 1,200 users. Retention 2x higher for AI users.'),
            dict(title='Feature 2: AI Writing Assistant — GA', date='2025-05-23', status='complete', cat='Engineering',
                 source='https://github.com/org/ai-platform/pull/74', source_name='PR #74 — Writing GA',
                 desc='Shipped to all users across web and mobile. 41% of active users engaged within first week. "Most-loved" in quarterly user survey.'),
            dict(title='SOC 2 AI Addendum', date='2025-06-06', status='complete', cat='Legal',
                 source='https://docs.google.com/document/d/soc2-ai-addendum', source_name='SOC 2 AI Addendum',
                 desc='SOC 2 Type II audit scope extended to cover AI data handling. Auditor sign-off received. Enterprise customers notified.'),
            dict(title='Feature 3: Intelligent Search — Beta', date='2025-06-27', status='complete', cat='Engineering',
                 source='https://github.com/org/ai-platform/pull/98', source_name='PR #98 — AI Search',
                 desc='Semantic search replacing keyword search across all content types. Hybrid retrieval (BM25 + embeddings). Beta: 800 users. Relevance score: 4.4/5.'),
            dict(title='Feature 3: Intelligent Search — GA', date='2025-07-25', status='complete', cat='Engineering',
                 source='https://github.com/org/ai-platform/pull/113', source_name='PR #113 — Search GA',
                 desc='Shipped to 100% of users. Search-to-action conversion up 54%. Legacy keyword search retired.'),
            dict(title='AI Cost Optimisation Sprint', date='2025-08-08', status='complete', cat='Engineering',
                 source='https://docs.google.com/spreadsheets/d/ai-cost-tracker', source_name='AI Cost Tracker',
                 desc='LLM spend audited and optimised. Prompt compression, model routing (small models for simple tasks), and batching reduced monthly cost by 38%.'),
            dict(title='Feature 4: Predictive Workflow Automation — Beta', date='2025-09-19', status='in-progress',
                 cat='Engineering',
                 source='https://github.com/org/ai-platform/pull/134', source_name='PR #134 — Automation Beta',
                 desc='AI-suggested workflow automations based on user behaviour patterns. Beta with 300 power users. Early signal: 22% reduction in repetitive manual tasks.'),
            dict(title='Feature 4: Predictive Workflow Automation — GA', date='2025-10-31', status='pending',
                 cat='Engineering',
                 source='https://docs.google.com/document/d/automation-spec', source_name='Automation Product Spec',
                 desc='Full rollout pending beta feedback cycle and safety review sign-off. Targeting Halloween release for marketing narrative.'),
            dict(title='AI Annual Review & 2026 Roadmap', date='2025-11-21', status='pending', cat='Planning',
                 source='https://docs.google.com/presentation/d/ai-2026-roadmap', source_name='AI 2026 Roadmap',
                 desc='Full year retrospective on AI programme impact. 2026 roadmap covering on-device models, personalisation engine, and agentic features.'),
            dict(title='Enterprise AI Tier Launch', date='2025-12-12', status='pending', cat='Growth',
                 source='https://docs.google.com/document/d/enterprise-ai-tier', source_name='Enterprise AI Tier Spec',
                 desc='New Enterprise AI add-on tier with higher rate limits, custom model fine-tuning, and dedicated support. Target: 50 enterprise customers by Q1 2026.'),
        ]
        for m in milestones:
            Milestone.objects.create(project=p, **m)

        events = [
            dict(title='Dr. Mei Lin joins as Head of AI', date='2025-01-06', etype='hire', people='Dr. Mei Lin',
                 source='https://docs.google.com/document/d/offer-mei', source_name='Offer Letter',
                 desc='Mei joins from Google DeepMind to lead the AI programme. She will own model selection, AI ethics, and the feature roadmap.'),
            dict(title='Claude selected as primary LLM provider', date='2025-01-24', etype='tech',
                 people='Dr. Mei Lin',
                 source='https://docs.google.com/document/d/llm-eval', source_name='LLM Evaluation Report',
                 desc='Anthropic Claude selected after evaluation across accuracy, safety, latency, and enterprise data privacy terms. API contract signed.'),
            dict(title='Tariq Osei joins as ML Engineer', date='2025-02-10', etype='hire', people='Tariq Osei',
                 desc='Tariq joins to build the embedding pipeline, vector search infrastructure, and model fine-tuning workflows.'),
            dict(title='AI ethics framework approved', date='2025-02-07', etype='note', people='Dr. Mei Lin',
                 source='https://docs.google.com/document/d/ai-ethics', source_name='AI Ethics Framework',
                 desc='Framework ratified by CTO, CPO, and General Counsel. Establishes mandatory bias testing, explainability requirements, and user opt-out rights for all AI features.'),
            dict(title='LLM spend tracking system built', date='2025-02-21', etype='tech', people='Tariq Osei',
                 source='https://github.com/org/ai-platform/pull/8', source_name='PR #8 — LLM Gateway',
                 desc='Internal cost dashboard live. Real-time per-feature, per-model cost breakdown. Alerts for spend anomalies. Semantic caching immediately saves ~$4k/month.'),
            dict(title='Prompt injection vulnerability found and patched', date='2025-03-28', etype='risk',
                 people='Dr. Mei Lin, Security',
                 source='https://docs.google.com/document/d/prompt-injection-report', source_name='Security Report',
                 desc='Internal red-team found prompt injection vector in summarisation beta. Input sanitisation and output validation layer added. Re-tested and cleared April 2.'),
            dict(title='Writing Assistant wins "Feature of the Quarter"', date='2025-06-16', etype='note',
                 people='Dr. Mei Lin',
                 desc='AI Writing Assistant voted Feature of the Quarter by all-hands. 41% weekly active usage rate — highest of any feature launched this year.'),
            dict(title='Nina Kozlov joins as AI Product Manager', date='2025-07-07', etype='hire',
                 people='Nina Kozlov',
                 desc='Nina joins to own the AI product roadmap, user research for AI features, and enterprise tier go-to-market.'),
            dict(title='Model hallucination rate spike — mitigated', date='2025-08-04', etype='risk',
                 people='Dr. Mei Lin, Tariq Osei',
                 source='https://docs.google.com/document/d/hallucination-incident', source_name='Incident Report',
                 desc='Claude API update caused 3x increase in hallucination rate on summarisation. Rolled back to pinned model version within 2 hours. Model version pinning policy introduced.'),
            dict(title='SOC 2 AI addendum — audit passed', date='2025-06-06', etype='note', people='Dr. Mei Lin',
                 desc='External auditors confirmed AI data handling meets SOC 2 Type II requirements. Enterprise sales unblocked for regulated industries.'),
            dict(title='AI cost reduction: 38% savings achieved', date='2025-08-08', etype='tech',
                 people='Tariq Osei',
                 desc='Optimisation sprint complete. Model routing, prompt compression, and request batching collectively reduce monthly LLM spend from $28k to $17k.'),
            dict(title='Enterprise AI tier pricing finalised', date='2025-11-10', etype='note',
                 people='Nina Kozlov, CFO',
                 source='https://docs.google.com/document/d/enterprise-pricing', source_name='Enterprise Pricing Doc',
                 desc='Enterprise AI tier priced at $25/seat/mo (minimum 50 seats). Early-adopter pricing of $18/seat/mo for first 6 months. Sales enablement materials in progress.'),
        ]
        for e in events:
            Event.objects.create(project=p, **e)

        self.stdout.write(f'  ✓ {p.name} — {len(milestones)} milestones, {len(events)} events')
