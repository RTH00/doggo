from dateutil.tz import UTC
from django.test import TestCase

from main.submodels.account import *


class SubmodelsAccountTests(TestCase):

    def test_create_account(self):
        account1: Account = create_account(datetime(year=2000, month=1, day=1, tzinfo=UTC))
        account1.save()
        account2: Account = create_account(datetime(year=2000, month=1, day=2, tzinfo=UTC))
        account2.save()
        self.assertIsNotNone(account1.id)
        self.assertEqual(str(account1.created_at), '2000-01-01 00:00:00+00:00')
        self.assertEqual(str(account1.last_seen_at), '2000-01-01 00:00:00+00:00')

        self.assertIsNotNone(account2.id)
        self.assertEqual(str(account2.created_at), '2000-01-02 00:00:00+00:00')
        self.assertEqual(str(account2.last_seen_at), '2000-01-02 00:00:00+00:00')

    def test_create_account_empty_inventory(self):
        account1: Account = create_account(datetime(year=2000, month=1, day=1, tzinfo=UTC))
        account1.save()
        self.assertIsNotNone(account1.id)
        self.assertEqual(account1.number_fitness_cookie, 1)
        self.assertEqual(account1.number_magic_bone, 1)
        self.assertEqual(account1.number_tennis_ball, 1)

    def test_fetch_account(self):
        account: Account = create_account2('toto', datetime(year=2000, month=1, day=1, tzinfo=UTC))
        account.save()
        self.assertIsNotNone(fetch_account('toto'))
        self.assertEqual(fetch_account('toto').id_secret, 'toto')
