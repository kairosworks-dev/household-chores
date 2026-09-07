# Design System

A deliberately small system for a two-person chore app. The most common interaction is
one person checking off a chore on a phone, so mobile comes first and touch targets
matter more than anything else here.

## Approach

- Server-rendered Django templates extending a single `base.html`
- One handwritten stylesheet at `static/css/app.css` — no framework, no build step
- Tokens as CSS custom properties on `:root`; components use the tokens, never raw values
- Progressive enhancement: everything works without JavaScript

## Tokens

```css
:root {
  /* Surfaces & text */
  --bg:        #f7f7f5;
  --surface:   #ffffff;
  --text:      #1c1c1a;
  --text-muted:#6b6b66;
  --border:    #e2e2dd;

  /* Accent — primary actions */
  --accent:      #2f6f4f;
  --accent-hover:#255a40;
  --accent-text: #ffffff;

  /* Status */
  --overdue: #b3261e;
  --today:   #8a5a00;
  --done:    #6b6b66;

  /* Spacing — 4px base */
  --s1: 4px;  --s2: 8px;  --s3: 12px;
  --s4: 16px; --s5: 24px; --s6: 32px;

  /* Type */
  --font: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --t-sm: 0.875rem; --t-base: 1rem; --t-lg: 1.125rem; --t-xl: 1.5rem;

  --radius: 6px;
  --tap: 44px;   /* minimum touch target */
}
```

Dark mode is out of scope for the MVP. If added later, redefine the surface, text, and
border tokens under `@media (prefers-color-scheme: dark)` and leave everything else alone.

## Layout

- Single column, `max-width: 640px`, centred, `--s4` padding
- No sidebar, no responsive breakpoint gymnastics — the phone layout is the desktop
  layout with more whitespace
- Vertical rhythm from the spacing scale only

## Components

**Chore row** — the core component. A checkbox, the title, and the assignee's name on
one line; due date underneath in `--text-muted` at `--t-sm`. The whole row is at least
`--tap` tall. The checkbox is a real `<input type="checkbox">` inside a POST form, not a
link, so it cannot be triggered by a prefetch.

**Status** — conveyed by a coloured left border on the row plus a text label, never by
colour alone: overdue uses `--overdue`, due today `--today`, upcoming the default
`--border`. Completed rows go `--text-muted` with a strikethrough title.

**Buttons** — one primary (filled `--accent`), one secondary (bordered, transparent),
one destructive (text in `--overdue`). Minimum height `--tap`. Destructive actions
confirm first.

**Forms** — label above input, full width, `--radius` corners, `--s3` padding. Errors
appear beneath the field in `--overdue` with the field border matching. Never rely on
placeholder text as a label.

**Flash messages** — a single bar under the header, `--surface` background with a
coloured left border matching the message level. Dismissible, and never the only place
important information appears.

**Empty states** — every list needs one. A short sentence plus the primary action, e.g.
"No chores yet." with an *Add a chore* button.

## Accessibility

These are non-negotiable and cheap to get right from the start:

- Every input has a real `<label>`; the chore checkbox is labelled by the chore title
- Visible focus ring on every interactive element — never `outline: none`
- Body text meets 4.5:1 contrast; the tokens above are chosen to pass
- Status is always text plus colour, never colour alone
- Page has one `<h1>`; headings descend without skipping

## Conventions

- Class names describe the thing, not the styling: `.chore-row`, not `.flex-between`
- No inline styles in templates
- Add a token before adding a one-off value; if a value is used once, it probably
  belongs in the component rule rather than in `:root`
- When unsure, remove something — the app has four screens and should feel like it
