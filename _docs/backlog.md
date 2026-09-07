# Backlog: Shared Chore Manager

> **Frozen.** Each task below is now a GitHub issue of the same number, and the
> issue is the system of record. This file is kept as the original index; it is
> not updated when an issue is groomed or changed.

Derived from [plan.md](plan.md). Each task is sized for a single session and written
to be picked up by someone who has not read the other tasks.

**Baseline as of writing:** the repo contains an empty Django 6.1 scaffold — a `config`
project package (settings, urls, asgi/wsgi), a registered but empty `chores` app, and
Django's built-in auth/sessions/admin tables migrated into SQLite. There are no models,
views, URLs, templates, or tests of our own yet. Dependencies between tasks are stated
inside each description rather than assumed.

**Two ordering constraints worth knowing before you start anything:** task 2 (custom user
model) must land before any other model is migrated, and task 3 (environment settings)
should land before any API key enters the codebase.

---

## 1. Set up the test harness and a smoke test
Goal: Get one passing test running with a single command.
Description: Add pytest and pytest-django to the project, configure them to find Django's
settings, and write a smoke test that requests a new `/healthz/` endpoint returning a
200 with the string "ok". This proves the whole loop — routing, view, test runner —
works end to end and gives every later task a green baseline to build on.

## 2. Replace the default User with a custom email-based user model
Goal: Users authenticate with an email address instead of a username.
Description: Create a `User` model in a new `accounts` app subclassing `AbstractUser`,
set `USERNAME_FIELD = "email"`, drop the `username` field, and point `AUTH_USER_MODEL`
at it. Because Django cannot swap the user model after other models have migrated, this
must be done before any other model exists — delete the local `db.sqlite3` and re-run
`migrate` as part of the task.

## 3. Move settings into environment variables
Goal: No secrets or environment-specific values are hardcoded in `settings.py`.
Description: Read `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, and `DATABASE_URL` from the
environment, with development-friendly defaults, and add a committed `.env.example`
documenting each one. The generated `SECRET_KEY` is currently in git history as
plaintext, so generate a fresh one and keep it out of version control.

## 4. Model the Household and its membership
Goal: A `Household` exists and users can belong to exactly one.
Description: Add a `Household` model with a name and creation timestamp, plus a
membership relation linking users to it. Enforce the plan's two-person limit at the
model or validation layer, and cover creation, membership, and the size cap with tests.

## 5. Model chores
Goal: A `Chore` row can represent both a one-off and a recurring chore.
Description: Add a `Chore` model belonging to a household, with a title, optional notes,
an assignee (a household member), a due date/time, and fields distinguishing a one-off
from a recurring chore. Assignment is always manual, so the assignee is a plain nullable
foreign key with no auto-selection logic.

## 6. Model completion logging
Goal: Marking a chore done records who did it and when.
Description: Add a `CompletionLog` model referencing a chore, the user who completed it,
and a timestamp, so history survives even after a recurring chore rolls over to its next
occurrence. Include tests that a log row is created with the right user and time, and
that a chore can be completed more than once over its lifetime.

## 7. Build signup, login, and logout
Goal: A person can create an account and sign in with email and password.
Description: Wire up Django's auth views with email-based forms, add templates for
signup, login, and logout, and redirect authenticated users to a placeholder dashboard.
Cover the happy path and a wrong-password rejection with tests.

## 8. Create and join a household on first login
Goal: A new user without a household is guided to create one.
Description: Add a view that prompts a user with no household to name and create one,
making them its first member, then redirects to the dashboard. Users who already belong
to a household should skip this screen entirely.

## 9. Model and generate household invites
Goal: An invite record with a unique, expiring token can be created.
Description: Add an `Invite` model holding the target email address, the inviting user,
the household, a cryptographically random token, a creation time, and an expiry. Include
tests for token uniqueness and for correctly reporting an expired invite.

## 10. Configure email sending
Goal: The app can send an email, printed to the console in development.
Description: Set the email backend from the environment — console for local development,
a real SMTP or API backend for production — and add a small helper for sending a
templated email. Verify with a test using Django's `locmem` backend that a message lands
in the outbox with the expected recipient and subject.

## 11. Send a household invitation by email
Goal: One user can invite their partner by entering an email address.
Description: Add a form and view that creates an invite for a given email address and
sends it a message containing a tokenized acceptance link. Guard against inviting someone
into a household that is already full, and against inviting an address that already has a
pending invite.

## 12. Accept an invitation
Goal: Clicking an invite link joins the recipient to the household.
Description: Add a view that validates an invite token, then either signs the recipient in
or walks them through signup, and finally adds them to the inviting household and marks
the invite used. Reject tokens that are expired, already used, or unrecognised with a
clear message rather than an error page.

## 13. Scope every query to the current user's household
Goal: A user can never see or modify another household's data.
Description: Add a reusable mixin or helper that filters chore querysets by the requesting
user's household, and apply it wherever chores are read or written. This is the single
security boundary in the app, so cover it with tests that a user from one household gets a
404 rather than a 403 when reaching for another's chore.

## 14. Create, edit, and delete chores
Goal: Either household member can manage any chore.
Description: Add forms and views for creating, editing, and deleting a chore, including
picking the assignee from household members and setting a due date. The plan specifies
equal permissions, so the only access check is household membership — not authorship.

## 15. Build the chore list dashboard
Goal: The home screen shows the household's chores grouped by status.
Description: Add a dashboard view listing the household's chores split into overdue, due
today, upcoming, and completed, showing each chore's assignee and due time. This is the
screen users see most, so it is worth getting the grouping and empty states right here
rather than iterating later.

## 16. Mark a chore complete from the list
Goal: A checkbox marks a chore done and records the completion.
Description: Add an endpoint that toggles a chore's completion, writing a `CompletionLog`
row and, for a recurring chore, advancing it to its next occurrence. Use a POST form
rather than a link so completion is not triggered by a crawler or a prefetch.

## 17. Expand recurring chores into due occurrences
Goal: A recurring chore knows its next due date after being completed.
Description: Implement the recurrence rules the plan calls for — daily, weekly, and a
custom interval — as a function that takes a chore and its last completion and returns the
next due datetime. Test the boundaries explicitly: month ends, and a chore completed late
versus early.

## 18. Send scheduled reminder emails
Goal: A chore that is due soon triggers an email to its assignee.
Description: Add a `send_reminders` management command that finds chores due inside a
configurable window, emails each assignee, and records that a reminder was sent so the
same one is never sent twice. Being runnable from cron keeps this testable and avoids a
broker for a two-person app.

## 19. Send a manual nudge
Goal: One user can prompt the other about a specific chore.
Description: Add a button on each chore that emails its assignee a nudge from the other
household member. Rate-limit it to something like one nudge per chore per hour so the
feature cannot be used to spam a partner's inbox.

## 20. Show reminders in the app
Goal: Pending reminders and nudges are visible on opening the app.
Description: Add an in-app notification model or derived query surfacing due chores and
received nudges as a banner or list on the dashboard, with a way to dismiss them. The plan
puts browser push notifications out of scope, so this is the in-app half of delivery only.

## 21. Add a responsive base template and styling
Goal: The app is usable on a phone and on a desktop.
Description: Add a base template with a mobile-first stylesheet, navigation, and flash
message rendering, then make the existing templates extend it. Checkboxes and buttons need
comfortable touch targets, since marking chores done on a phone is the app's most common
interaction.

## 22. Register models in the Django admin
Goal: Data can be inspected and fixed without a database client.
Description: Register the household, chore, completion, and invite models with sensible
list displays, filters, and search fields. This is a small task that pays for itself the
first time an invite or a recurrence needs debugging.

## 23. Add a deployment configuration
Goal: The app runs somewhere other than a laptop.
Description: Add a production settings path, a WSGI/ASGI server, static file handling via
WhiteNoise, and a Postgres connection driven by `DATABASE_URL`, plus a short deploy note
in the README. Include the cron entry that runs the reminder command from task 18.
