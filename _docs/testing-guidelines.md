# Testing Guidelines

This is a learning project, not production software. The goal is enough testing to
catch real mistakes and to make each backlog task verifiably "done" — not a coverage
percentage.

## Tools

- **pytest** + **pytest-django** as the runner (set up in task 1)
- Django's own test client for views; no browser automation
- SQLite in-memory for the test database
- No factory library — plain helper functions are enough for a two-model-deep app

## Layout

Tests live in a `tests/` package inside each app, one file per concern:

```
accounts/tests/test_models.py     accounts/tests/test_auth.py
chores/tests/test_models.py       chores/tests/test_views.py
                                  chores/tests/test_recurrence.py
```

Delete the `tests.py` that `startapp` generates when you create the package.

## Running

```
uv run pytest                  # everything
uv run pytest chores           # one app
uv run pytest -k recurrence    # one topic
uv run pytest -x -q            # stop at first failure, quiet
```

Every commit should leave the suite green.

## What to test

Test **your** logic and the decisions in [plan.md](plan.md):

- **Model rules you wrote** — a household caps at two members, an invite expires,
  a completion log records the right user and time.
- **Recurrence math** — the highest-value tests in the project. Cover month ends,
  a chore completed late, and one completed early.
- **Household scoping** — the app's only security boundary. A user from household A
  requesting household B's chore must get a 404. Test this on every chore view.
- **View happy path plus one failure** — the page loads for a logged-in member; an
  anonymous visitor is redirected to login.
- **Email side effects** — assert against `django.core.mail.outbox`, never send real
  mail from a test.

## What not to test

- Django itself — that a `CharField` stores a string, that `ForeignKey` cascades
- The admin, beyond it loading
- Exact HTML or CSS; assert on status codes, redirects, and content the user reads
- Third-party libraries

## Conventions

- Name tests as sentences: `test_completing_a_recurring_chore_sets_next_due_date`.
- One behaviour per test. If the name needs "and", split it.
- Use `@pytest.mark.django_db` on anything touching the database.
- Put shared setup in `conftest.py` fixtures — a `user`, a `household`, a `chore`
  fixture will cover most of the suite.
- Freeze time with a fixed `datetime` passed into the function rather than mocking
  the clock. Recurrence functions should take "now" as an argument for exactly this
  reason.
- Prefer a boring assertion over a clever one; a failing test should say what broke
  without needing the debugger.

## Definition of done for a backlog task

1. The behaviour in the issue's Goal works when clicked through by hand.
2. There is at least one test covering that behaviour and one covering its main
   failure mode.
3. `uv run pytest` is green.
