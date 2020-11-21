from typing import Optional

from django.http import HttpRequest

from main.submodels import account
from main.submodels.account import Account

COOKIE_ACCOUNT_ID_SECRET = 'account_id_secret'


def get_account_secret_id(request: HttpRequest) -> Optional[str]:
    return request.COOKIES.get(COOKIE_ACCOUNT_ID_SECRET)


def fetch_account(request: HttpRequest) -> Optional[Account]:
    return account.fetch_account(get_account_secret_id(request))
