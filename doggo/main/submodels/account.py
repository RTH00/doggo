from datetime import timedelta
from typing import Optional

from django.db import models
from django.db.models.functions.datetime import datetime

from main.utils import token

COOKIE_CONSENT_DURATION: timedelta = timedelta(days=365)


class Account(models.Model):

    class Meta:
        db_table = 'accounts'
    id = models.BigAutoField(auto_created=True, primary_key=True)
    id_secret = models.TextField(null=True)
    created_at = models.DateTimeField(null=True)
    last_seen_at = models.DateTimeField(null=True)
    cookie_consent_at: datetime = models.DateTimeField(null=True)
    # inventory
    number_magic_bone: int = models.BigIntegerField(default=1)
    number_fitness_cookie: int = models.BigIntegerField(default=1)
    number_tennis_ball: int = models.BigIntegerField(default=1)

    # TODO test
    def is_cookie_consent_valid(self, now: datetime) -> bool:
        return self.cookie_consent_at is not None and self.cookie_consent_at + COOKIE_CONSENT_DURATION > now

    def update_last_seen_at(self, new_last_seen_at: datetime):
        self.last_seen_at = new_last_seen_at


def create_account2(id_secret: str, created_at: datetime) -> Account:
    return Account(
        id_secret=id_secret,
        created_at=created_at,
        last_seen_at=created_at
    )


def create_account(created_at: datetime) -> Account:
    return create_account2(token.random_token(200), created_at)


def fetch_account(id_secret: str) -> Optional[Account]:
    if id_secret is None:
        return None
    return Account.objects.filter(id_secret=id_secret).first()
