---
description: Groom a GitHub issue into a well-formed task
argument-hint: <issue number>
---

Launch the `pm` subagent to groom issue #$ARGUMENTS. Do not groom it yourself -
`_docs/process.md` makes the main session the orchestrator, and the orchestrator
does not do the work of a role it dispatches.

Tell the agent to do everything `_docs/team/pm.md` describes except the final
`gh issue edit`: research the issue, decide what moves out of scope, write the
rewritten body to a file, and report that body back along with what it intends
to file as follow-ups.

Show me that body. On my approval, message the same agent to apply it - it files
the follow-up issues and edits issue #$ARGUMENTS itself, so the PM stays the role
that touches the issue.
