# Himmah — هِمَّة

> A personal operating system for focused, intentional work.

---

## What It Is

Most productivity tools track tasks. Himmah tracks *days* — how you planned them, how they actually went, and whether you're making progress on the things that matter.

The problem I kept running into: I'd end a day not knowing if it was good or bad, productive or wasted. I had tasks ticked off but no signal on whether the day moved me toward anything real. I had goal-tracking apps that felt disconnected from my daily execution. I had journalling apps that had no awareness of what I'd actually done.

Himmah is one system that holds all of it together — the plan you make the night before, the tasks you execute during the day, the honest review you write at the end, and the long-term goals everything is supposed to feed into.

I use it every day. It is not a demo.

---

## Why I Built This

I spent months bouncing between Notion, Todoist, and paper notebooks, never finding something that felt like it was mine. Everything either tracked tasks in isolation or asked me to manage a second job just to maintain the system. I wanted something that felt like a cockpit — one screen to start the day, one screen to close it, and a real record of where my time actually went. I built Himmah because the alternative was to keep losing days to tools that weren't designed around how I actually think and work. The fact that it's running on my own server and stores none of my data with a third party is not a coincidence.

---

## System Pages

| Page | Purpose |
|------|---------|
| **Today** | Daily execution screen — active tasks, timers, goal progress, morning ratings |
| **Plan** | Night-before contract — set tomorrow's tasks, intentions, and week overview |
| **Goals** | Everything you're building toward — primary goal, categories, target hours, logged progress |
| **Review** | End-of-day honest mirror — score (1–5), energy level, what you got done, gratitude note |
| **Gate** | Commitment gate for new ideas — forces you to see what you're trading before you start something new |
| **Settings** | User account management |

---

## Tech Stack

### Backend
| Technology | Version | Role |
|------------|---------|------|
| Python | 3.x | Runtime |
| Django | 6.0.4 | Web framework |
| Django REST Framework | 3.17.1 | REST API layer |
| djangorestframework-simplejwt | 5.5.1 | JWT authentication |
| PostgreSQL | — | Primary database |
| psycopg2-binary | 2.9.11 | PostgreSQL driver |
| django-cors-headers | 4.9.0 | CORS configuration |
| python-dotenv | 1.2.2 | Environment management |

### Frontend
| Technology | Version | Role |
|------------|---------|------|
| Next.js | 16.2.3 | React framework (App Router) |
| React | 19.2.4 | UI layer |
| TypeScript | 5.x | Type safety |
| Tailwind CSS | 4.x | Styling |
| Axios | 1.15.0 | HTTP client with interceptors |

---

## Features

### Authentication
- User registration and login
- JWT access tokens (1-day lifetime) with refresh tokens (7-day lifetime)
- Automatic token rotation and blacklisting on refresh
- Client-side auto-refresh — expired tokens are renewed transparently without re-login
- Rate limiting: 10 req/min on login, 5 req/min on registration

### Task Management
- Tasks linked to specific dates, goals, and day plans
- Drag-order support within a day (`order` field)
- Built-in timer: `start_timer` / `stop_timer` actions calculate actual time spent
- Estimated vs actual minutes tracked per task
- Mark done with timestamp, or skip with a reason
- Per-task reflection notes (what went well, what was missed)

### Goals
- Goals with categories: professional, spiritual, family, health
- Status tracking: active, completed, paused, pivoted
- Primary goal designation — surfaced on the Today screen
- Target hours and logged hours (summed from completed tasks)
- Hierarchical goals: sub-goals link to a parent goal

### Planning
- Day plans with intentions and `niyyah` (purpose) fields
- Morning ratings at plan creation: energy, clarity, sleep (all 1–5)
- Week calendar view across plans

### Review
- Daily reviews: score (1–5), energy level, distraction log, gratitude note
- Weekly reviews: what worked, what didn't, focus for next week
- Auto-calculated stats: average energy, average score, best/worst day of week

### Gate (Distraction Management)
- Log new ideas and impulses before acting on them
- Verdict system: `parked` (auto-revisit in 48h), `pivot`, or `rejected`
- Forces deliberate decision-making instead of reactive context-switching

---

## API Reference

All endpoints require `Authorization: Bearer <access_token>` unless noted.

**Base URL:** `http://localhost:8000/api`

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/token/` | Login — returns `{access, refresh, username}` |
| `POST` | `/token/refresh/` | Refresh access token |
| `POST` | `/auth/register/` | Register new user |

### Goals

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/goals/` | List goals — filter: `?is_primary=true`, `?status=active` |
| `POST` | `/goals/` | Create goal |
| `GET` | `/goals/{id}/` | Retrieve goal |
| `PATCH` | `/goals/{id}/` | Update goal |
| `DELETE` | `/goals/{id}/` | Delete goal |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/tasks/` | List tasks — filter: `?date=YYYY-MM-DD` or `?start=&end=` |
| `POST` | `/tasks/` | Create task |
| `GET` | `/tasks/{id}/` | Retrieve task |
| `PATCH` | `/tasks/{id}/` | Update task |
| `DELETE` | `/tasks/{id}/` | Delete task |
| `POST` | `/tasks/{id}/start_timer/` | Start task timer |
| `POST` | `/tasks/{id}/stop_timer/` | Stop timer — writes `actual_mins` |
| `POST` | `/tasks/{id}/mark_done/` | Mark task complete |

### Day Plans

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dayplans/` | List — filter: `?date=YYYY-MM-DD` |
| `POST` | `/dayplans/` | Create |
| `GET/PATCH/DELETE` | `/dayplans/{id}/` | Retrieve, update, delete |

### Day Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/dayreviews/` | List |
| `POST` | `/dayreviews/` | Submit review |
| `GET/PATCH/DELETE` | `/dayreviews/{id}/` | Retrieve, update, delete |

### Week Reviews

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/weekreviews/` | List |
| `POST` | `/weekreviews/` | Submit review |
| `GET/PATCH/DELETE` | `/weekreviews/{id}/` | Retrieve, update, delete |

### Reflections

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/reflections/` | List |
| `POST` | `/reflections/` | Create reflection on a task |
| `GET/PATCH/DELETE` | `/reflections/{id}/` | Retrieve, update, delete |

### Distractions (Gate)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/distractions/` | List logged distractions |
| `POST` | `/distractions/` | Log new distraction |
| `GET/PATCH/DELETE` | `/distractions/{id}/` | Retrieve, update, delete |

---

## Database Models

### Goal
```
id              BigAutoField (PK)
user            FK → User (CASCADE)
title           CharField(255)
category        CharField(100)
status          CharField — choices: active | completed | paused | pivoted
is_primary      BooleanField
parent_goal     FK → Goal (self-referential, nullable)
target_hours    DecimalField(6,2)
start_date      DateField
target_date     DateField
created_at      DateTimeField (auto)
updated_at      DateTimeField (auto)

computed: logged_hours() — sum of actual_mins on completed tasks linked to this goal
```

### Task
```
id                BigAutoField (PK)
user              FK → User (CASCADE)
goal              FK → Goal (nullable)
day_plan          FK → DayPlan (nullable)
title             CharField(255)
scheduled_date    DateField
order             PositiveIntegerField
estimated_mins    PositiveIntegerField
actual_mins       PositiveIntegerField (nullable)
timer_started_at  DateTimeField (nullable)
timer_ended_at    DateTimeField (nullable)
done              BooleanField
done_at           DateTimeField (nullable)
skipped           BooleanField
skip_reason       TextField
```

### DayPlan
```
id                BigAutoField (PK)
user              FK → User (CASCADE)
date              DateField
intention         TextField
niyyah_for_allah  TextField
niyyah_for_self   TextField
morning_energy    PositiveSmallIntegerField (1–5, nullable)
morning_clarity   PositiveSmallIntegerField (1–5, nullable)
sleep_quality     PositiveSmallIntegerField (1–5, nullable)

unique_together: (user, date)
```

### DayReview
```
id              BigAutoField (PK)
user            FK → User (CASCADE)
date            DateField
score           PositiveSmallIntegerField (1–5)
reflection      TextField
energy_level    PositiveSmallIntegerField
distracted_by   TextField
gratitude_note  TextField
barakah_felt    BooleanField
barakah_note    TextField

computed: completed_count(), total_count()
unique_together: (user, date)
```

### WeekReview
```
id                BigAutoField (PK)
user              FK → User (CASCADE)
week_start        DateField
week_end          DateField
score             PositiveSmallIntegerField
what_worked       TextField
what_didnt        TextField
focus_next_week   TextField
average_energy    DecimalField(3,2, nullable)
average_score     DecimalField(3,2, nullable)
best_day          PositiveSmallIntegerField (weekday enum, nullable)
worst_day         PositiveSmallIntegerField (weekday enum, nullable)

unique_together: (user, week_start)
```

### Distraction
```
id              BigAutoField (PK)
user            FK → User (CASCADE)
goal            FK → Goal (nullable)
title           CharField(255)
description     TextField
triggered_at    DateTimeField
verdict         CharField — choices: parked | pivot | rejected (nullable)
verdict_reason  TextField
reviewed_at     DateTimeField (nullable)
revisit_after   DateField (nullable — auto-set to triggered_at + 48h)
```

### Reflection
```
id              BigAutoField (PK)
user            FK → User (CASCADE)
task            OneToOneField → Task (CASCADE)
note            TextField
what_went_well  TextField
what_missed     TextField
```

---

## Running Locally

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL running locally

### Backend setup

```bash
cd himmah/backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Fill in: SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Backend runs at `http://127.0.0.1:8000`

### Frontend setup

```bash
cd himmah/frontend

npm install
npm run dev
```

Frontend runs at `http://127.0.0.1:3000`

### Environment variables

**Backend (`.env`):**
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=himmah
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### Get an API token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

---

## Project Status

**Status: Active — in daily personal use**

The core system is complete and stable. I use it every day to plan, execute, and review my work.

What works:
- Full authentication (register, login, token refresh)
- Complete CRUD across all resources
- Task timers with actual vs estimated time tracking
- Daily and weekly review cycles
- Goal hierarchy and progress tracking
- Gate system for distraction capture

What's in progress:
- Deployment to a VPS (currently local only)
- Analytics dashboard — weekly trends, consistency streaks
- Mobile responsiveness improvements

---

## Project Structure

```
himmah/
├── backend/
│   ├── core/               Django settings and root URLs
│   ├── himmah/             Main app — models, views, serializers, URLs
│   ├── requirements.txt
│   └── manage.py
└── frontend/
    ├── src/
    │   ├── app/            Pages (App Router) — today, plan, review, goals, gate
    │   ├── components/     Shell, Nav, TimePill
    │   └── lib/            API client, auth helpers, TypeScript types
    ├── package.json
    └── next.config.ts
```

---

*Himmah (هِمَّة) — Arabic for ambition, resolve, and the inner drive to pursue something worthwhile.*
