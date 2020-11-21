from datetime import datetime, timedelta

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from doggo import settings
from main.submodels.account import COOKIE_CONSENT_DURATION, Account, create_account
from main.utils.cookie import COOKIE_ACCOUNT_ID_SECRET, fetch_account


def set_account_id_cookie(response: HttpResponse, account_id: str, now: datetime) -> HttpResponse:
    response.set_cookie(
        key=COOKIE_ACCOUNT_ID_SECRET,
        value=account_id,
        expires=now + timedelta(days=365 * 2),
        secure=settings.SESSION_COOKIE_SECURE
    )
    return response


def cookie_consent(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        now: datetime = timezone.now()
        account: Account = fetch_account(request)
        if account is None:
            account = create_account(created_at=now)
        account.cookie_consent_at = now
        account.save()
        response: HttpResponse = redirect('/')
        return set_account_id_cookie(response, account.id_secret, now)
    else:
        return render(request, 'cookie_consent.html', {
            'disable_navbar': True,
            'cookie_consent_duration_days': str(COOKIE_CONSENT_DURATION.days)
        })
