- Tasks are GitHub issues, one at a time
- Read the acceptance criteria before starting and before closing
- New issues follow `_docs/task-template.md`
- Work on `main`; no branches or pull requests for this project
- Commit regularly

Roles
- PM - grooms a task before anyone implements it, follows _docs/team/pm.md
- Engineer - implements one groomed task, follows _docs/team/software-engineer.md
- QA - checks the result against the acceptance criteria, follows _docs/team/qa-engineer.md

Orchestrator

The main session is the orchestrator. It launches the PM, the engineer
and QA as subagents. It does not groom, implement or test itself.

Lifecycle

1. Pick the next open GitHub issue
2. PM grooms it
3. Engineer implements it
4. QA verifies it
5. On FAIL, back to step 3 with the QA comment as input
6. On PASS, close the issue
7. Repeat until the backlog is empty

Rules

- Do not skip step 2
- Groom once. Step 5 returns to step 3, never to step 2 - the criteria an
  engineer started against do not move underneath them
- If the engineer or QA reports that an acceptance criterion is wrong,
  impossible, or contradicts another, stop the loop and go back to step 2 for a
  re-groom. That is the only thing that reopens grooming
- After three FAIL verdicts on one issue, stop and hand it to the human rather
  than starting a fourth pass
- The engineer does not close the issue
- QA does not fix the code, only outputs PASS or FAIL
- The orchestrator closes the issue only after QA outputs PASS

The GitHub issue is the system of record. `_docs/backlog.md` is the original
index, is not kept in sync, and is not edited as part of any task.
