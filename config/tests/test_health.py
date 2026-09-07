"""Smoke test for the project.

This is the baseline every later task builds on: routing, a view and Django's
test client working end to end. It must stay free of `@pytest.mark.django_db`
so that it keeps passing while #2 replaces the user model.
"""

from django.urls import reverse


def test_healthz_returns_ok(client):
    response = client.get('/healthz/')

    assert response.status_code == 200
    assert response.content == b'ok'


def test_healthz_is_reachable_by_its_url_name():
    assert reverse('healthz') == '/healthz/'
