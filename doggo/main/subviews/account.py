from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from main.submodels.account import Account
from main.subviews.cookie_consent import set_account_id_cookie
from main.utils.cookie import fetch_account


@never_cache
@csrf_protect
def render_account(request: HttpRequest) -> HttpResponse:
    account: Account = fetch_account(request)
    update_account_absolute_link: str = str(request.scheme) \
                                        + "://" \
                                        + str(request.get_host()) \
                                        + str(reverse('change_account', kwargs={'account_secret_id': account.id_secret}))
    return render(request, 'account.html', context={
        'account': account,
        'update_account_absolute_link': update_account_absolute_link
    })


@never_cache
@csrf_protect
def render_change_account(request: HttpRequest, account_secret_id: str = '') -> HttpResponse:
    now: datetime = timezone.now()
    return set_account_id_cookie(redirect('account'), account_secret_id, now)
