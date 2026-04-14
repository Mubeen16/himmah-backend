# Himmah — Product Roadmap
> هِمَّة — the soul's drive to elevate

## Vision
A personal operating system for a Muslim engineer to execute his daily 
commitments, track long term goals, and protect his focus from distraction.
Not a todo app. A commitment engine rooted in Islamic values and modern 
psychology. Built for one person first. Built for the world eventually.

## The person this is built for
- A self-building engineer — backend, ML, systems
- A Muslim — niyyah before every action, muraqabah every evening
- A family man — family time is as important as coding time
- Someone who starts things and needs a system stronger than willpower

## Core philosophy
- Every task traces back to a goal
- Every day has a contract, an execution, and an honest review
- New ideas go through a gate — pivot or park, never just start
- A correct execution of the plan makes you who you are
- Barakah is real — track the conditions that bring it

---

## Project Structure
```
himmah/
├── frontend/          Next.js 15 + TypeScript + Tailwind CSS
├── backend/           Django 6 + Django REST Framework
└── ROADMAP.md         single source of truth
```

## Tech Stack
```
Frontend    Next.js 15 + TypeScript + Tailwind CSS
Backend     Django 6 + Django REST Framework
Database    PostgreSQL 17
Auth        JWT — djangorestframework-simplejwt
HTTP Client Axios
```

## Data Model
```
Goal          long term commitments with target hours
Task          daily execution linked to goals
DayPlan       nightly contract — intention + niyyah + morning state
DayReview     end of day mirror — score + reflection + barakah
WeekReview    weekly pattern — best day, worst day, average
Reflection    per task learning — what went well, what missed
Distraction   new idea gate — park, pivot, or reject
```

## API Endpoints
```
POST   /api/token/                    get JWT tokens
POST   /api/token/refresh/            refresh access token
GET    /api/goals/                    list goals
POST   /api/goals/                    create goal
PATCH  /api/goals/{id}/               update goal
DELETE /api/goals/{id}/               delete goal
GET    /api/tasks/                    list tasks
GET    /api/tasks/?date=YYYY-MM-DD    tasks for a date
POST   /api/tasks/                    create task
PATCH  /api/tasks/{id}/               update task
DELETE /api/tasks/{id}/               delete task
POST   /api/tasks/{id}/start_timer/   start timer
POST   /api/tasks/{id}/stop_timer/    stop timer
POST   /api/tasks/{id}/mark_done/     mark done
GET    /api/dayplans/                 list day plans
POST   /api/dayplans/                 create day plan
PATCH  /api/dayplans/{id}/            update day plan
GET    /api/dayreviews/               list reviews
POST   /api/dayreviews/               create review
PATCH  /api/dayreviews/{id}/          update review
GET    /api/weekreviews/              list week reviews
POST   /api/weekreviews/              create week review
GET    /api/reflections/              list reflections
POST   /api/reflections/              create reflection
PATCH  /api/reflections/{id}/         update reflection
GET    /api/distractions/             list distractions
POST   /api/distractions/             create distraction
PATCH  /api/distractions/{id}/        update verdict
```

---

## Phase 1 — Foundation (localStorage) ✅ DONE
> Goal: get the daily loop working on one machine

- [x] Project created — Next.js + TypeScript + Tailwind
- [x] Data types defined — types.ts
- [x] localStorage layer — storage.ts
- [x] Plan page — night before contract
- [x] Today page — morning execution, mark done
- [x] Review page — end of day honest score

---

## Phase 2 — Real Backend ✅ DONE
> Goal: production grade backend with real database

- [x] Django project created — core/
- [x] Himmah app created
- [x] PostgreSQL connected
- [x] Models built:
  - Goal — title, category, status, parent_goal, target_hours, start_date, target_date
  - Task — title, scheduled_date, order, estimated_mins, actual_mins, timer, done, skipped
  - DayPlan — date, intention, niyyah_for_allah, niyyah_for_self, morning_energy, morning_clarity, sleep_quality
  - DayReview — date, score, reflection, energy_level, distracted_by, gratitude_note, barakah_felt, barakah_note
  - WeekReview — week_start, week_end, score, what_worked, what_didnt, focus_next_week, best_day, worst_day
  - Reflection — task, note, what_went_well, what_missed
  - Distraction — title, description, triggered_at, verdict, verdict_reason, revisit_after
- [x] JWT authentication — access token 1 day, refresh 7 days, rotate enabled
- [x] Serializers — all 7, computed fields, nested data
- [x] ViewSets — all 7, user scoped, timer actions on Task
- [x] URLs — all endpoints registered under /api/
- [x] Admin — all models registered
- [x] CORS configured — localhost:3000 and localhost:3001
- [x] DB constraints enforced — energy/score 1-5 at database level
- [x] 4 migrations applied cleanly

---

## Phase 3 — Frontend Connected to Backend 🔄 IN PROGRESS
> Goal: replace localStorage with real API, full auth flow

- [x] Project restructured — frontend/ and backend/ under one himmah/ root
- [x] ROADMAP.md at root — single source of truth
- [x] Axios installed
- [x] API client — src/lib/api.ts with JWT interceptors, auto token refresh
- [x] Auth service — src/lib/auth.ts login/logout/isAuthenticated
- [ ] Login page — src/app/login/page.tsx
- [ ] Middleware — route protection, cookie based auth
- [ ] Update Today page — fetch tasks from /api/tasks/?date=today
- [ ] Update Plan page — POST to /api/dayplans/ and /api/tasks/
- [ ] Update Review page — POST to /api/dayreviews/
- [ ] Goals page — view and create long term goals
- [ ] Remove all localStorage logic from storage.ts

---

## Phase 4 — Core Experience 📋 PLANNED
> Goal: Himmah feels like what it was designed to be

### Navigation
- [ ] Persistent nav bar — هِمَّة · today · plan · goals · review
- [ ] Active state on current page
- [ ] Mobile responsive nav

### Today screen
- [ ] Journey bar — week X of Y toward destination
- [ ] Task cards showing goal they serve — ↳ backend engineer · week 14
- [ ] Task timer — start/stop, auto calculates actual_mins
- [ ] Mark done updates goal logged_hours automatically
- [ ] Progress bar — tasks done vs total
- [ ] Remaining time display
- [ ] Empty state — honest message if no plan was made

### Plan screen
- [ ] Night before contract builder
- [ ] Niyyah fields — for Allah, for self
- [ ] Morning state fields — energy, clarity, sleep (filled in morning)
- [ ] Link each task to a goal via dropdown
- [ ] Drag to reorder tasks
- [ ] Total committed hours warning if over 8hrs
- [ ] Commit button disabled until intention + at least one task

### Goals screen
- [ ] View all active goals grouped by category
- [ ] Progress bar — logged hours vs target hours
- [ ] On track / behind indicator
- [ ] Days remaining to target date
- [ ] Create new goal
- [ ] Edit and pause goals
- [ ] Child goals — year → month → week cascade view

### Review screen
- [ ] End of day score 1-5
- [ ] Honest reflection text
- [ ] Gratitude note
- [ ] Barakah felt toggle + note
- [ ] Energy level
- [ ] What distracted you
- [ ] Missed tasks warning — "your tomorrow self carries this"
- [ ] Auto link to plan tomorrow after submit

### Distraction gate
- [ ] Log new idea — title and description
- [ ] Show current streak and journey position
- [ ] Verdict — pivot, park, reject
- [ ] Revisit date shown automatically — 48hr default
- [ ] Parked ideas list with revisit dates
- [ ] Pivot flow — link to existing or new goal

### Reflection
- [ ] Per task reflection after marking done
- [ ] What went well
- [ ] What you missed
- [ ] Timestamp shown

---

## Phase 5 — Patterns and Insight 📋 PLANNED
> Goal: Himmah shows you who you actually are over time

- [ ] Weekly review screen
- [ ] Weekly pattern — best day, worst day, average energy
- [ ] Goal progress over time — hours logged per week chart
- [ ] Streak tracking — consecutive days with score >= 3
- [ ] Distraction log history — parked vs pivoted vs rejected
- [ ] Monthly summary — what you built this month
- [ ] Barakah pattern — what conditions correlate with your best days
- [ ] Consistency score — how often you plan the night before
- [ ] Time accuracy — estimated vs actual mins over time

---

## Phase 6 — Polish and Production 📋 PLANNED
> Goal: something you are proud to show

- [ ] Full dark mode — every page, every component
- [ ] Responsive design — works on tablet
- [ ] Arabic typography — هِمَّة branding throughout
- [ ] Loading states on all async operations
- [ ] Error handling — network failures, server errors, form validation
- [ ] Empty states — every page has a meaningful empty state
- [ ] Environment variables — .env.local for frontend, .env for backend
- [ ] Django deployed — Railway or Render
- [ ] Next.js deployed — Vercel
- [ ] Custom domain — himmah.app
- [ ] SSL — HTTPS everywhere
- [ ] Data export — your data is yours, CSV or JSON

---

## Phase 7 — Multi User 📋 FUTURE
> Goal: other people can use Himmah

- [ ] Registration page
- [ ] Email verification
- [ ] Password reset flow
- [ ] User onboarding — set your identity and goals on first login
- [ ] Privacy — all data strictly user scoped, verified at every endpoint
- [ ] Rate limiting on API
- [ ] Admin dashboard — usage stats

---

## Phase 8 — Product 📋 FUTURE
> Goal: Himmah becomes something real in the world

- [ ] Landing page — what is Himmah, who is it for
- [ ] Waitlist with email capture
- [ ] Feedback system inside the app
- [ ] Blog — building in public, the philosophy behind Himmah
- [ ] Mobile app — React Native
- [ ] Push notifications — plan reminder at night, morning intention
- [ ] Community — others on the same path
- [ ] Himmah for teams — accountability between people
- [ ] Himmah for organisations — Islamic institutions, bootcamps

---

## Decisions Log
> Why we made key decisions

| Decision | Why |
|----------|-----|
| Django over Node.js | Mubeen is a Python engineer. Build in your strength. |
| PostgreSQL over MongoDB | Relational data. Goals link to tasks link to plans. |
| JWT over sessions | Stateless. Works for mobile later. |
| localStorage first | Ship fast, validate the concept, migrate to API later. |
| No logged_hours stored | Computed from tasks. Never stale. |
| Cookie + localStorage for token | Middleware needs cookie. Axios needs localStorage. |
| 48hr distraction revisit | Psychology — 80% of ideas lose urgency in 48hrs. |
| Barakah tracking | No Western app tracks this. Unique to Himmah. |

---

## Notes for Agents
> Read this before writing any code

1. This is a personal operating system, not a todo app
2. Every endpoint is user scoped — always filter by request.user
3. Never store computed values — logged_hours, completed_count calculated live
4. Token stored in both localStorage (for axios) and cookie (for Next.js `proxy.ts` auth gate)
5. Backend runs on port 8000, frontend on port 3000
6. All API calls go through src/lib/api.ts — never use fetch directly
7. Check ROADMAP.md phase completion before starting new features
8. When in doubt — ask before building
