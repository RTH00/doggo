from datetime import datetime

from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils import timezone

from main.submodels.account import Account
from main.utils.cookie import fetch_account

COOKIE_CONSENT_PATH: str = 'cookie_consent'
PRIVACY_POLICY_PATH: str = 'legal/privacy_policy'
TERMS_AND_CONDITIONS_PATH: str = 'legal/terms_and_conditions'
CONTACT_PATH: str = 'legal/contact'

WHITELIST_WITHOUT_COOKIE = [
    '/' + COOKIE_CONSENT_PATH,
    '/' + PRIVACY_POLICY_PATH,
    '/' + TERMS_AND_CONDITIONS_PATH,
    '/' + CONTACT_PATH
]


class CookieConsentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request: HttpRequest):
        if request.path in WHITELIST_WITHOUT_COOKIE:
            return self.get_response(request)
        else:
            now: datetime = timezone.now()
            account: Account = fetch_account(request)
            if account is not None and account.is_cookie_consent_valid(now):
                account.update_last_seen_at(now)
                account.save()
                return self.get_response(request)
            else:
                return redirect(COOKIE_CONSENT_PATH)
