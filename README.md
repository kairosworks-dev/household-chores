# Household Chores

AI Dev Tools Zoomcamp — Module 1 homework.

A working exercise in **spec-driven, multi-agent development**, following
[AI-Native Development: Specifications](https://aishippingblog.com/p/ai-native-development-specifications).
The app itself is real but secondary; the point is the process that builds it.

## Context

The article's premise: coding agents now write faster than anyone can review, so
the bottleneck moved from typing to **saying precisely what you want and checking
what came back**. Given a vague task, a strong agent will confidently build
something polished and wrong. The remedy is a spec detailed enough that the agent
has no gaps to fill with assumptions, plus specialised roles that hand work to
each other through defined checkpoints.

Four ideas from the article that this repo puts into practice:

- **Spec-driven development** — write the specification before any code
- **Context engineering** — make the right information reachable across sessions
  (`AGENTS.md`, `_docs/`, GitHub issues)
- **Loop engineering** — define stop conditions so an agent knows when it is done
- **Graph engineering** — specialised agents at each stage, with explicit handoffs

## The project

A web app for two people sharing a household to track chores, completions and
reminders. Scope is frozen in [`_docs/plan.md`](_docs/plan.md): manual assignment
only, recurring and one-off chores, completion logging with timestamp and person,
scheduled and manual reminders by email and in-app, a household capped at two
members linked by email invite. Explicitly out of MVP: analytics, push
notifications, photo proof, streaks, auto-assignment.

Stack: Python 3.13, Django 6.1 managed with `uv`, SQLite locally and Postgres in
production, server-rendered templates with one handwritten stylesheet and no
frontend build, pytest + pytest-django.

### How work is organised

| Document | Role |
|---|---|
| [`_docs/plan.md`](_docs/plan.md) | Project scope. Frozen |
| [`_docs/backlog.md`](_docs/backlog.md) | The original 23-task index. Frozen; GitHub issues are the system of record |
| [`_docs/task-template.md`](_docs/task-template.md) | Goal / Acceptance criteria / Out of scope / Constraints |
| [`_docs/process.md`](_docs/process.md) | The lifecycle and the rules that bound it |
| [`_docs/team/`](_docs/team/) | One document per role — PM, engineer, QA |
| [`_docs/testing-guidelines.md`](_docs/testing-guidelines.md) | What to test, what not to, and the conventions |
| [`_docs/design-system.md`](_docs/design-system.md) | Required reading for anything on screen |

The main session is the **orchestrator**. It grooms nothing, implements nothing
and tests nothing — it dispatches `pm`, `software-engineer` and `qa-engineer` as
subagents (`.claude/agents/`) and closes the issue when QA returns a PASS.

## Current status

**Issue #1 — Set up the test harness and a smoke test: done and closed**, having
run the full lifecycle end to end. PM groomed it, the engineer implemented it, QA
verified it independently and returned PASS on all nine acceptance criteria, and
the orchestrator closed it. `uv run pytest` is green (2 passed) with a `/healthz/`
endpoint, a test that deliberately needs no database, and no `chores/tests.py`
stub.

**Issue #4 — Model the Household and its membership: groomed, not started.** The
grooming surfaced that it is blocked on #2 (the custom user model must migrate
first) *and* on #1, which the filer had not noticed.

**Next: #2**, the custom email-based `User` model. It is the hard ordering
constraint — Django cannot swap the user model once another model has migrated —
and #4, #5, #6, #8 and #9 all sit behind it.

27 issues open. #24–#28 were filed as follow-ups during grooming and QA rather
than being silently dropped.

**One thing outstanding:** the `pm` subagent cannot run `gh issue create` or
`gh issue edit`, which is the whole of what its role document asks it to do. The
fix is a `.claude/settings.json` with those two Bash allow rules; it has to be
written by a human, for the reason in the next section.

## Lessons

### From the article

Most of it held up in practice. The three role documents transferred almost
verbatim, the four-section task template is the right shape, and issue-as-system-
of-record kept every session grounded without needing to re-explain anything.

### What we had to work out ourselves

**The published lifecycle has a dead end.** "On FAIL, back to the engineer" loops
forever if the acceptance criterion itself is wrong — and the engineer's own role
document tells them to *report* a bad criterion rather than implement around it,
with nowhere for that report to go. We added a re-groom trigger (a wrong,
impossible or contradictory criterion is the only thing that reopens grooming)
and a three-failure escalation to a human. A loop needs an exit that isn't
success.

**Groom once.** Nothing in the original said so, and re-running the PM on each
pass would move the criteria out from under an engineer who is forbidden to move
them himself.

**Choose tools so the constraints are real, not advisory.** QA's role says
"nothing in the code was changed" — so the `qa-engineer` agent has no `Write` or
`Edit`, and a role that cannot write cannot drift into fixing what it was sent to
measure. The engineer is the only role that can write. Where tooling *can't*
enforce a rule — Bash can still run `gh issue close`, which the engineer is
forbidden to do — say so in prose rather than pretending the tool list covers it.

**A slash command can quietly contradict the process.** `/groom` said "act as the
Product Manager", which made the orchestrator become the PM — against its own
rule that it does not groom. It now dispatches the subagent. The review gate
survived by having the PM write its draft to a file and report back *without*
applying, then resuming that same agent on approval, so the PM stays the role
that touches the issue.

**Permissions are the real limit on agent autonomy.** The PM was blocked from
`gh issue create` and correctly refused to route around the denial — leaving the
groom unapplied and the orchestrator to finish it by hand, breaking the very
separation we had just built. Then writing the settings file to grant that
permission was itself blocked, which is *correct*: an agent widening its own
permissions is privilege escalation, and that boundary is worth more than the
convenience. A role is only as autonomous as its tool grants, and some of those
grants can only come from a human.

**Declined is not the same as deferred.** The PM role says everything moved out
of scope links to a follow-up issue. But some things are refused on principle —
coverage thresholds, which `testing-guidelines.md` rejects outright — and filing
an issue for those would misrepresent the decision as postponed. Out-of-scope
sections now distinguish the two.

**Independent QA earns its keep.** It was given the issue number and nothing
else — deliberately not briefed on what the engineer had reported. It
reconstructed the `runserver` recreates `db.sqlite3` trap on its own and
correctly attributed it to Django's migration check rather than the view, found
three coverage gaps that no acceptance criterion required (filed as #27), and
noticed `requires-python = ">=3.12"` contradicting `.python-version` (#28).
Pre-loading it with the engineer's framing would have bought a faster PASS and a
worthless one.

**Grooming is where ordering constraints surface.** #4 read like an
implementable task until someone had to write down what "a household has members"
depends on.
