from datetime import datetime

from dateutil.tz import UTC
from django.http import HttpRequest
from django.test import TestCase, RequestFactory

from main.submodels.account import create_account, Account, create_account2
from main.submodels.dog import create_dog, BreedType
from main.subviews import home

from main.utils.cookie import COOKIE_ACCOUNT_ID_SECRET


class SubviewsHomeTests(TestCase):
    def test_render_home_1(self):
        """
        Test without any dog
        :return:
        """
        create_account2('secret_toto', datetime(year=2000, month=1, day=1, tzinfo=UTC)).save()

        request: HttpRequest = RequestFactory().get('home')
        request.COOKIES[COOKIE_ACCOUNT_ID_SECRET] = 'secret_toto'
        home.render_home(request)

    def test_render_home_2(self):
        """
        Test with one dog
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('secret_toto', created_at)
        account.save()
        create_dog(account, 'dog_id', created_at, 'name', BreedType.GOLDEN_RETRIEVER).save()
        request: HttpRequest = RequestFactory().get('home')
        request.COOKIES[COOKIE_ACCOUNT_ID_SECRET] = 'secret_toto'
        home.render_home(request)
