"""Project-level views.

`healthz` is infrastructure rather than a feature: it answers "is this process
up and serving requests?" for a human with curl or a hosting platform's probe.
It deliberately touches nothing else — no database, no template, no session.
"""

from django.http import HttpResponse


def healthz(request):
    """Return a plain `ok`, with no trailing newline, for a liveness check."""
    return HttpResponse('ok', content_type='text/plain; charset=utf-8')
