# Project Scope: Shared Chore Manager

A web app for managing shared household chores between two users (partners), with manual assignment, completion tracking, and reminders.

## Users & Access
- Simple login (email/password) per user
- Household of 2, linked via **email invite** (one user invites the other by email)
- **Equal permissions** — either user can create, edit, delete, or reassign any chore

## Chores
- **Manually assigned** to a person (no auto-assignment/rotation/claiming)
- Support both:
  - **Recurring chores** (daily/weekly/custom schedule)
  - **One-off chores** (added as needed, no repeat)

## Tracking
- Checkbox to mark a chore as done
- Records **timestamp** and **who completed it**

## Reminders
- **Scheduled reminders** based on due date/time (automatic)
- **Manual nudge** — either user can trigger a reminder for a specific chore
- Delivered via:
  - **In-app** (visible when the app is opened)
  - **Email**

## Platform
- **Responsive web app** (single codebase, works across devices via browser)
- Shared backend/database for real-time-ish sync between both users

## Explicitly Out of Scope (MVP)
- No stats/fairness dashboard or analytics
- No browser push notifications
- No photo proof of completion
- No streak/status tracking beyond done/not done
- No claim-based or rule-based auto-assignment

## Suggested Next Steps
1. Define the data model (Users, Households, Chores, CompletionLogs, Invites)
2. Choose the tech stack (frontend framework, backend, database, email service)
3. Design core screens (login/signup, household setup, chore list, add/edit chore)
4. Plan the reminder/scheduling mechanism (cron job, scheduled function, etc.)
