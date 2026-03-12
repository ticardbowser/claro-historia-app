from django.core.management.base import BaseCommand
from tracker.models import Project, Milestone, Event


class Command(BaseCommand):
    help = 'Seeds the database with a full year of sample data'

    def handle(self, *args, **options):
        project, created = Project.objects.get_or_create(pk=1, defaults={'name': 'Website Redesign'})
        if not created:
            project.name = 'Website Redesign'
            project.save()

        Milestone.objects.filter(project=project).delete()
        Event.objects.filter(project=project).delete()

        # ── Milestones ─────────────────────────────────────────────────────────
        milestones = [
            # Q1 — Discovery & Design
            dict(title='Project Kickoff', date='2025-01-08', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/kickoff-brief', source_name='Kickoff Brief',
                 desc='Align stakeholders on scope, timeline, and success metrics. Kick off ceremony held with 14 attendees across Product, Engineering, and Marketing.'),
            dict(title='Stakeholder Interviews Complete', date='2025-01-20', status='complete', cat='Research',
                 source='https://docs.google.com/document/d/stakeholder-interview-notes', source_name='Interview Notes',
                 desc='12 stakeholder interviews conducted across 5 departments. Key themes: speed, mobile experience, SEO visibility, and brand refresh.'),
            dict(title='Discovery & User Research', date='2025-01-31', status='complete', cat='Research',
                 source='https://docs.google.com/presentation/d/research-findings', source_name='Research Findings Deck',
                 desc='User interviews, competitive analysis, and heuristic evaluation of current site. 22 user sessions recorded and synthesised.'),
            dict(title='Analytics Audit', date='2025-02-07', status='complete', cat='Research',
                 source='https://docs.google.com/spreadsheets/d/analytics-audit', source_name='Analytics Audit Sheet',
                 desc='Full GA4 and Hotjar audit. Top exit pages identified: /pricing, /contact, /docs/getting-started. Average session duration 1m 42s.'),
            dict(title='Information Architecture', date='2025-02-14', status='complete', cat='Design',
                 source='https://www.figma.com/file/ia-sitemap', source_name='Figma — Sitemap',
                 desc='New sitemap reduces top-level navigation from 9 items to 5. Content audit completed; 34% of pages flagged for consolidation or removal.'),
            dict(title='Design System & Component Library', date='2025-02-28', status='complete', cat='Design',
                 source='https://www.figma.com/file/design-system', source_name='Figma — Design System',
                 desc='Component library, typography scale, colour tokens, spacing system, and motion principles. 62 components documented.'),
            dict(title='High-Fidelity Wireframes — Marketing Pages', date='2025-03-10', status='complete', cat='Design',
                 source='https://www.figma.com/file/wireframes-marketing', source_name='Figma — Marketing Wireframes',
                 desc='Home, About, Pricing, and Contact pages completed in desktop and mobile breakpoints.'),
            dict(title='High-Fidelity Wireframes — Product Pages', date='2025-03-21', status='complete', cat='Design',
                 source='https://www.figma.com/file/wireframes-product', source_name='Figma — Product Wireframes',
                 desc='Dashboard, Onboarding flow, Settings, and Docs hub wireframes complete. Accessibility annotations added.'),
            dict(title='Stakeholder Design Review', date='2025-03-28', status='complete', cat='Review',
                 source='https://docs.google.com/presentation/d/design-review-deck', source_name='Design Review Deck',
                 desc='Sign-off received from CMO and CPO. 7 revision requests logged; 5 resolved same day. Pricing page layout to be revisited in Q2.'),

            # Q2 — Build
            dict(title='Development Environment & CI Setup', date='2025-04-04', status='complete', cat='Engineering',
                 source='https://github.com/org/website-redesign', source_name='GitHub Repo',
                 desc='Monorepo configured with Turborepo. GitHub Actions CI pipeline running lint, type-check, and unit tests on every PR. Vercel preview deployments enabled.'),
            dict(title='Design Tokens & Theme Integration', date='2025-04-11', status='complete', cat='Engineering',
                 source='https://github.com/org/website-redesign/pull/12', source_name='PR #12 — Tokens',
                 desc='Design tokens exported from Figma via Style Dictionary. Dark mode support built in from day one.'),
            dict(title='Component Library — Core Atoms', date='2025-04-25', status='complete', cat='Engineering',
                 source='https://github.com/org/website-redesign/pull/31', source_name='PR #31 — Atoms',
                 desc='Button, Input, Badge, Tag, Avatar, Spinner, and Tooltip components shipped. Storybook published to internal staging.'),
            dict(title='Marketing Pages — Frontend Build', date='2025-05-09', status='complete', cat='Engineering',
                 source='https://github.com/org/website-redesign/pull/54', source_name='PR #54 — Marketing',
                 desc='Home, About, Pricing, and Contact pages built and responsive. Lighthouse scores: Performance 94, Accessibility 98, SEO 100.'),
            dict(title='CMS Integration (Contentful)', date='2025-05-16', status='complete', cat='Engineering',
                 source='https://docs.google.com/document/d/cms-integration-spec', source_name='CMS Integration Spec',
                 desc='Blog, changelog, and docs hub connected to Contentful. Editorial team onboarded and first 12 articles migrated.'),
            dict(title='Product Pages — Frontend Build', date='2025-05-30', status='complete', cat='Engineering',
                 source='https://github.com/org/website-redesign/pull/89', source_name='PR #89 — Product Pages',
                 desc='Dashboard shell, Onboarding flow, and Settings pages built. Integration with auth provider complete.'),
            dict(title='Internal QA Round 1', date='2025-06-06', status='complete', cat='QA',
                 source='https://docs.google.com/spreadsheets/d/qa-round-1', source_name='QA Tracker — Round 1',
                 desc='48 issues logged across browsers and devices. P0: 2, P1: 9, P2: 37. All P0s resolved within 48 hours.'),
            dict(title='Performance & SEO Optimisation', date='2025-06-20', status='complete', cat='Engineering',
                 source='https://docs.google.com/document/d/perf-seo-report', source_name='Perf & SEO Report',
                 desc='Image pipeline migrated to next/image with automatic WebP/AVIF. LCP improved from 3.8s to 1.2s. Structured data added to all product pages.'),
            dict(title='Docs Hub & Knowledge Base Build', date='2025-06-27', status='complete', cat='Engineering',
                 source='https://github.com/org/website-redesign/pull/112', source_name='PR #112 — Docs Hub',
                 desc='Full docs hub with search (Algolia), versioning, and sidebar navigation. 240 legacy docs pages migrated with redirects.'),

            # Q3 — Pre-launch
            dict(title='Accessibility Audit (WCAG 2.1 AA)', date='2025-07-11', status='complete', cat='QA',
                 source='https://docs.google.com/document/d/accessibility-audit-report', source_name='Accessibility Audit Report',
                 desc='Third-party accessibility audit by Deque Systems. 14 issues found; all resolved and re-tested. Site certified WCAG 2.1 AA compliant.'),
            dict(title='Security Review & Pen Test', date='2025-07-18', status='complete', cat='Engineering',
                 source='https://docs.google.com/document/d/security-review', source_name='Security Review Report',
                 desc='External penetration test completed. 1 medium and 3 low severity findings; all patched. CSP headers and HSTS configured.'),
            dict(title='Internal UAT — Stakeholder Sign-off', date='2025-07-25', status='complete', cat='Review',
                 source='https://docs.google.com/spreadsheets/d/uat-sign-off', source_name='UAT Sign-off Sheet',
                 desc='User acceptance testing with 8 internal stakeholders. All acceptance criteria met. Final green light granted by CPO and CTO.'),
            dict(title='Content Freeze & Final Copy Review', date='2025-08-01', status='complete', cat='Content',
                 source='https://docs.google.com/document/d/copy-review-final', source_name='Final Copy Review Doc',
                 desc='All copy locked for launch. Legal reviewed Terms, Privacy Policy, and Cookie Notice. Brand team approved all imagery.'),
            dict(title='Redirect Map & SEO Migration Plan', date='2025-08-08', status='complete', cat='Engineering',
                 source='https://docs.google.com/spreadsheets/d/redirect-map', source_name='Redirect Map',
                 desc='301 redirects mapped for 318 legacy URLs. Crawl budget and canonical strategy documented. Google Search Console property configured.'),
            dict(title='Staging Environment Final Review', date='2025-08-15', status='complete', cat='QA',
                 source='https://docs.google.com/spreadsheets/d/qa-round-2', source_name='QA Tracker — Round 2',
                 desc='Full regression pass on staging. 12 minor issues resolved. Load testing completed — site stable at 2,000 concurrent users.'),
            dict(title='Launch Runbook & Rollback Plan', date='2025-08-22', status='complete', cat='Planning',
                 source='https://docs.google.com/document/d/launch-runbook', source_name='Launch Runbook',
                 desc='Step-by-step launch runbook authored. Rollback procedure documented and tested. On-call rota confirmed for launch weekend.'),

            # Q3 — Launch
            dict(title='Soft Launch — Internal & Beta Users', date='2025-08-29', status='complete', cat='Launch',
                 source='https://docs.google.com/document/d/soft-launch-report', source_name='Soft Launch Report',
                 desc='New site opened to 500 beta users and all employees. 99.98% uptime over first 72 hours. 23 minor UX issues collected and triaged.'),
            dict(title='Public Launch', date='2025-09-03', status='complete', cat='Launch',
                 source='https://docs.google.com/presentation/d/launch-announcement', source_name='Launch Announcement Deck',
                 desc='Public launch across all channels. Press release distributed. Product Hunt launch achieved #3 product of the day. 18,400 unique visitors on day one.'),

            # Q4 — Post-launch
            dict(title='Post-launch Analytics Review', date='2025-09-19', status='complete', cat='Research',
                 source='https://docs.google.com/presentation/d/post-launch-analytics', source_name='Post-launch Analytics Deck',
                 desc='Bounce rate down 31%. Average session duration up to 3m 08s. Docs search usage 4x higher than legacy site. Conversion rate up 18%.'),
            dict(title='Performance Regression Check', date='2025-10-03', status='complete', cat='Engineering',
                 source='https://docs.google.com/spreadsheets/d/perf-regression-oct', source_name='Perf Regression — Oct',
                 desc='Monthly performance audit. All Core Web Vitals green. Third-party script audit reduced JS payload by 62KB.'),
            dict(title='Localisation — French & German', date='2025-10-24', status='in-progress', cat='Engineering',
                 source='https://github.com/org/website-redesign/pull/201', source_name='PR #201 — i18n',
                 desc='i18n framework (next-intl) integrated. French translation 80% complete. German translation in review. Launch targeted for mid-November.'),
            dict(title='A/B Test — Pricing Page Layout', date='2025-11-07', status='in-progress', cat='Growth',
                 source='https://docs.google.com/document/d/ab-test-pricing-spec', source_name='A/B Test Spec',
                 desc='Testing new value-proposition-first layout vs current feature-grid layout. Variant B showing +11% trial sign-up rate after 2 weeks. Reaching statistical significance Nov 21.'),
            dict(title='Localisation Launch — FR & DE', date='2025-11-21', status='pending', cat='Engineering',
                 desc='Go-live for French and German locales. Hreflang tags, locale-specific sitemaps, and regional redirects to be deployed.'),
            dict(title='Annual SEO Review', date='2025-12-05', status='pending', cat='Research',
                 source='https://docs.google.com/document/d/annual-seo-review', source_name='Annual SEO Review',
                 desc='Full SEO health check: crawl errors, backlink profile, keyword rankings vs targets, and Core Web Vitals trend report.'),
            dict(title='Q4 Retrospective & 2026 Roadmap', date='2025-12-12', status='pending', cat='Planning',
                 source='https://docs.google.com/presentation/d/2026-roadmap', source_name='2026 Roadmap Draft',
                 desc='Full project retrospective with all workstreams. Lessons learned documented. 2026 web roadmap presented to leadership for approval.'),
            dict(title='Year-End Handover to Web Team', date='2025-12-19', status='pending', cat='Planning',
                 source='https://docs.google.com/document/d/handover-doc', source_name='Handover Document',
                 desc='Full ownership transfer to the permanent web team. All documentation, credentials, and runbooks handed over. Project officially closed.'),
        ]

        for m in milestones:
            Milestone.objects.create(project=project, **m)

        # ── Events ─────────────────────────────────────────────────────────────
        events = [
            # January
            dict(title='Sarah Chen joins as Lead Designer', date='2025-01-06', etype='hire', people='Sarah Chen',
                 source='https://docs.google.com/document/d/offer-letter-sarah', source_name='Offer Letter',
                 desc='Sarah brings 8 years of product design experience from Figma and Shopify. She will lead the visual design track and own the design system.'),
            dict(title='Marcus Webb departs the project', date='2025-01-24', etype='depart', people='Marcus Webb',
                 source='https://mail.google.com/mail/u/0/#inbox/thread-marcus-offboarding', source_name='Offboarding Thread',
                 desc='Marcus transitioned to a new internal role in the Platform team. Frontend responsibilities redistributed to Priya Nair and Dev Kapoor.'),

            # February
            dict(title='Priya Nair joins as Frontend Engineer', date='2025-02-03', etype='hire', people='Priya Nair',
                 source='https://docs.google.com/document/d/offer-letter-priya', source_name='Offer Letter',
                 desc='Priya joins to backfill frontend capacity after Marcus\'s departure. She specialises in React performance and accessibility. Onboarding completed in 3 days.'),
            dict(title='Design team restructured under Engineering lead', date='2025-02-07', etype='reorg',
                 people='Sarah Chen, Priya Nair, Dev Kapoor',
                 source='https://docs.google.com/document/d/reorg-memo-feb2025', source_name='Reorg Memo — Feb 2025',
                 desc='Design and engineering merged into a single cross-functional pod to reduce handoff friction. Weekly design-dev syncs introduced every Tuesday.'),
            dict(title='Switched from Webpack to Vite', date='2025-02-12', etype='tech',
                 source='https://docs.google.com/spreadsheets/d/build-benchmarks', source_name='Build Benchmarks Sheet',
                 desc='Build times reduced from 42s to 4s (cold) and 180ms (HMR). All team members updated local environments within one day. CI pipeline updated.'),
            dict(title='Third-party mapping API rate limit risk flagged', date='2025-02-21', etype='risk', people='Dev Kapoor',
                 source='https://docs.google.com/document/d/api-risk-assessment', source_name='API Risk Assessment',
                 desc='The mapping API used on the Contact page has a 500 req/day free tier cap. An upgrade to the $49/mo plan or a request-caching strategy is needed before launch.'),

            # March
            dict(title='Jordan Kim joins as QA Engineer', date='2025-03-03', etype='hire', people='Jordan Kim',
                 source='https://docs.google.com/document/d/offer-letter-jordan', source_name='Offer Letter',
                 desc='Jordan joins for the build and pre-launch phases. She will own the QA tracker, write automated E2E tests in Playwright, and coordinate UAT.'),
            dict(title='Figma Enterprise licence approved', date='2025-03-10', etype='tech',
                 source='https://docs.google.com/document/d/figma-licence-approval', source_name='Licence Approval Memo',
                 desc='Finance approved the Figma Organisation plan ($75/editor/mo). Enables branching, advanced permissions, and Design System analytics for the team.'),
            dict(title='Scope change: Docs hub added to Phase 1', date='2025-03-17', etype='risk',
                 people='CPO, Dev Kapoor, Sarah Chen',
                 source='https://docs.google.com/document/d/scope-change-docs-hub', source_name='Scope Change Request',
                 desc='CPO requested the full docs hub be included in the September launch rather than deferred to Phase 2. Timeline reviewed and confirmed feasible with current headcount. Adds ~3 weeks of engineering work.'),
            dict(title='Alejandro Reyes joins as Content Strategist', date='2025-03-24', etype='hire',
                 people='Alejandro Reyes',
                 source='https://docs.google.com/document/d/offer-letter-alejandro', source_name='Offer Letter',
                 desc='Alejandro joins to own the content migration, CMS editorial workflow, and SEO copywriting for all new pages. Previously led content at HubSpot.'),

            # April
            dict(title='Contentful CMS selected over Sanity', date='2025-04-02', etype='tech',
                 people='Dev Kapoor, Alejandro Reyes',
                 source='https://docs.google.com/document/d/cms-evaluation', source_name='CMS Evaluation Report',
                 desc='After evaluating Contentful, Sanity, and Prismic, the team selected Contentful for its editorial UX, webhook support, and existing company familiarity. Contracts signed.'),
            dict(title='Vercel Enterprise contract signed', date='2025-04-09', etype='tech',
                 source='https://docs.google.com/document/d/vercel-contract', source_name='Vercel Contract',
                 desc='Moved from Vercel Pro to Enterprise for advanced edge config, DDoS protection, and 99.99% SLA uptime guarantee. Includes dedicated support.'),
            dict(title='Legacy site SEO baseline snapshot taken', date='2025-04-14', etype='note',
                 people='Alejandro Reyes',
                 source='https://docs.google.com/spreadsheets/d/seo-baseline', source_name='SEO Baseline Sheet',
                 desc='Full export of current keyword rankings, backlink profile, and Ahrefs domain authority taken for post-launch comparison. 1,842 indexed pages captured.'),

            # May
            dict(title='Dev Kapoor promoted to Tech Lead', date='2025-05-05', etype='reorg', people='Dev Kapoor',
                 source='https://docs.google.com/document/d/dev-promotion-memo', source_name='Promotion Memo',
                 desc='Dev takes on technical leadership of the full engineering workstream. He will conduct code reviews, own the architecture decisions, and be the primary engineering contact for stakeholders.'),
            dict(title='Algolia contract signed for Docs search', date='2025-05-12', etype='tech',
                 people='Dev Kapoor',
                 source='https://docs.google.com/document/d/algolia-contract', source_name='Algolia Contract',
                 desc='Algolia DocSearch selected for the knowledge base. Index will cover all docs, blog, and changelog pages. Estimated 4-hour indexing time post-launch.'),
            dict(title='Image CDN migration to Cloudflare', date='2025-05-19', etype='tech', people='Priya Nair',
                 source='https://github.com/org/website-redesign/pull/67', source_name='PR #67 — CDN Migration',
                 desc='All static assets migrated to Cloudflare R2 + Images. Average image load time reduced from 820ms to 95ms globally. Bandwidth costs estimated to drop 70%.'),

            # June
            dict(title='Brand refresh: updated logo and colour palette', date='2025-06-02', etype='note',
                 people='Sarah Chen, Marketing',
                 source='https://www.figma.com/file/brand-refresh', source_name='Figma — Brand Refresh',
                 desc='Marketing finalised a subtle brand refresh — new wordmark, updated primary palette (deeper teal, warmer off-white), and revised icon set. Design system updated to reflect changes.'),
            dict(title='Legal review: GDPR cookie compliance', date='2025-06-09', etype='risk',
                 people='Legal, Dev Kapoor',
                 source='https://docs.google.com/document/d/gdpr-review', source_name='GDPR Review',
                 desc='Legal flagged that current analytics setup requires explicit consent banners for EU visitors. OneTrust cookie consent banner integrated and tested. Sign-off received June 23.'),
            dict(title='Jordan Kim departs (contract end)', date='2025-06-20', etype='depart', people='Jordan Kim',
                 source='https://docs.google.com/document/d/jordan-offboarding', source_name='Offboarding Notes',
                 desc='Jordan\'s 4-month QA contract concluded. All test suites documented and handed to Dev Kapoor. Playwright E2E suite covers 94% of critical user flows.'),
            dict(title='Load testing completed — system stable', date='2025-06-27', etype='tech',
                 people='Dev Kapoor',
                 source='https://docs.google.com/document/d/load-test-results', source_name='Load Test Results',
                 desc='k6 load tests run at 500, 1000, and 2000 concurrent users. No errors at 2000 CCU. P95 response time 210ms. Auto-scaling confirmed working on Vercel Edge.'),

            # July
            dict(title='Deque Systems accessibility audit begins', date='2025-07-07', etype='note',
                 people='Sarah Chen, Priya Nair',
                 source='https://docs.google.com/document/d/deque-audit-brief', source_name='Deque Audit Brief',
                 desc='Third-party accessibility audit contracted with Deque Systems. Scope: all public-facing pages. Estimated 2-week turnaround. Team blocked no other work during audit period.'),
            dict(title='External pen test — 1 medium finding resolved', date='2025-07-18', etype='risk',
                 people='Dev Kapoor',
                 source='https://docs.google.com/document/d/pentest-report', source_name='Pen Test Report',
                 desc='Medium finding: insufficiently scoped CORS policy on the API route. Patched same day. 3 low findings (missing rate limiting, verbose error messages) resolved within 48 hours. Final sign-off received July 25.'),
            dict(title='Aisha Okonkwo joins as Growth Engineer', date='2025-07-28', etype='hire',
                 people='Aisha Okonkwo',
                 source='https://docs.google.com/document/d/offer-letter-aisha', source_name='Offer Letter',
                 desc='Aisha joins to own post-launch experimentation, A/B testing infrastructure (LaunchDarkly), and conversion optimisation. She will work across the web and product teams.'),

            # August
            dict(title='LaunchDarkly feature flag system integrated', date='2025-08-04', etype='tech',
                 people='Aisha Okonkwo, Dev Kapoor',
                 source='https://github.com/org/website-redesign/pull/178', source_name='PR #178 — Feature Flags',
                 desc='LaunchDarkly integrated for controlled rollouts and A/B tests. First flag controls the new pricing page layout. Enables % rollout to beta users before full release.'),
            dict(title='Final CPO & CTO sign-off received', date='2025-08-15', etype='note',
                 people='CPO, CTO, Dev Kapoor, Sarah Chen',
                 source='https://docs.google.com/document/d/final-sign-off', source_name='Sign-off Record',
                 desc='CPO and CTO formally signed off on the staging environment after the final UAT session. Green light to proceed with launch planning. No further scope changes permitted.'),
            dict(title='DNS cutover plan rehearsed', date='2025-08-25', etype='tech', people='Dev Kapoor',
                 source='https://docs.google.com/document/d/dns-cutover-runbook', source_name='DNS Cutover Runbook',
                 desc='Full DNS cutover rehearsed on a shadow domain. TTL reduced to 60s 48 hours before launch. Cloudflare, Vercel, and Mailgun records confirmed. Estimated cutover window: 3–5 minutes.'),

            # September
            dict(title='Public launch — site live', date='2025-09-03', etype='note',
                 people='Full team',
                 source='https://docs.google.com/presentation/d/launch-announcement', source_name='Launch Announcement Deck',
                 desc='The new site went live at 09:00 UTC. Zero downtime deployment. Product Hunt campaign launched simultaneously. #3 product of the day. 18,400 unique visitors in first 24 hours.'),
            dict(title='Post-launch P1 bug: mobile nav broken on iOS 16', date='2025-09-04', etype='risk',
                 people='Priya Nair',
                 source='https://github.com/org/website-redesign/issues/234', source_name='GitHub Issue #234',
                 desc='CSS scroll-lock bug caused mobile navigation to freeze on iOS 16 Safari. Hotfix deployed within 4 hours. Affected approximately 8% of launch-day traffic.'),
            dict(title='Alejandro Reyes transitions to part-time advisory', date='2025-09-15', etype='reorg',
                 people='Alejandro Reyes',
                 source='https://docs.google.com/document/d/alejandro-transition', source_name='Transition Memo',
                 desc='Content migration complete; Alejandro moves to 1 day/week advisory role. Day-to-day content operations handed to the Marketing team.'),
            dict(title='Google Search Console: 318 redirects confirmed indexed', date='2025-09-22', etype='note',
                 people='Alejandro Reyes',
                 source='https://docs.google.com/spreadsheets/d/gsc-indexing-report', source_name='GSC Indexing Report',
                 desc='All 318 redirected legacy URLs confirmed as crawled and resolved in GSC. No 404s in coverage report. Organic traffic recovering on expected trajectory.'),

            # October
            dict(title='Aisha Okonkwo presents growth experiment roadmap', date='2025-10-06', etype='note',
                 people='Aisha Okonkwo',
                 source='https://docs.google.com/presentation/d/growth-experiment-roadmap', source_name='Growth Experiment Roadmap',
                 desc='Q4 experimentation roadmap presented to leadership: 6 A/B tests planned across Pricing, Home hero, and Onboarding flow. Budget approved for 3 paid attribution studies.'),
            dict(title='Next.js upgraded to v15', date='2025-10-13', etype='tech', people='Dev Kapoor, Priya Nair',
                 source='https://github.com/org/website-redesign/pull/189', source_name='PR #189 — Next.js v15',
                 desc='Upgraded from Next.js 14 to 15. App Router fully adopted. Partial Prerendering enabled on marketing pages. Build time reduced by 22%.'),
            dict(title='Sara Chen wins internal Design Award', date='2025-10-20', etype='note', people='Sarah Chen',
                 source='https://docs.google.com/document/d/design-award-2025', source_name='Award Announcement',
                 desc='Sarah recognised at the annual internal design summit for the Claro Historia design system. The component library has since been adopted by two other product teams.'),

            # November
            dict(title='i18n framework integrated — FR & DE in progress', date='2025-11-03', etype='tech',
                 people='Priya Nair',
                 source='https://github.com/org/website-redesign/pull/201', source_name='PR #201 — i18n',
                 desc='next-intl integrated. URL structure uses locale prefixes (/fr, /de). Translation files managed in Phrase. French strings 80% complete; German in review with external agency.'),
            dict(title='A/B test: Pricing page variant B ahead', date='2025-11-10', etype='note',
                 people='Aisha Okonkwo',
                 source='https://docs.google.com/spreadsheets/d/ab-test-results', source_name='A/B Test Results',
                 desc='After 2 weeks and 12,000 visitors per variant, Variant B (value-proposition-first layout) shows +11% trial sign-up rate. Reaching 95% statistical significance on Nov 21.'),
            dict(title='Priya Nair promoted to Senior Frontend Engineer', date='2025-11-17', etype='reorg',
                 people='Priya Nair',
                 source='https://docs.google.com/document/d/priya-promotion', source_name='Promotion Memo',
                 desc='Priya promoted following exceptional performance during the build and post-launch phases. She takes on mentoring responsibilities for two new junior engineers joining in 2026.'),

            # December
            dict(title='Variant B pricing layout shipped to 100%', date='2025-12-01', etype='tech',
                 people='Aisha Okonkwo, Priya Nair',
                 source='https://github.com/org/website-redesign/pull/218', source_name='PR #218 — Pricing Layout',
                 desc='A/B test concluded with 97% statistical confidence. Variant B fully rolled out. Estimated +11% improvement in trial sign-up rate preserved. Feature flag removed.'),
            dict(title='2026 web roadmap submitted for budget approval', date='2025-12-08', etype='note',
                 people='Dev Kapoor, Aisha Okonkwo',
                 source='https://docs.google.com/presentation/d/2026-roadmap', source_name='2026 Roadmap Deck',
                 desc='2026 roadmap submitted to leadership covering: video integration, personalisation engine, mobile app deep-link landing pages, and expanded localisation to 8 languages. Budget decision expected Jan 2026.'),
        ]

        for e in events:
            Event.objects.create(project=project, **e)

        self.stdout.write(self.style.SUCCESS(
            f'Seeded project "{project.name}" with {len(milestones)} milestones and {len(events)} events.'
        ))
