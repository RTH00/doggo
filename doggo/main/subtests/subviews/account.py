from datetime import datetime, tzinfo

from dateutil.tz import UTC
from django.test import TestCase

from main.submodels.account import create_account, Account
from main.submodels.dog import create_dog, Dog, BreedType
from main.subviews.dogs import fetch_dogs


# TODO move fetch_dogs in right file
class SubviewsAccountTests(TestCase):

    def test_fetch_dogs_1(self):
        now: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        self.assertEqual(fetch_dogs(1, now), [])
        self.assertTrue(True)

    def test_fetch_dogs_2(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account(created_at)
        account.save()
        dog: Dog = create_dog(account, '1', created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.save()
        self.assertEqual(fetch_dogs(account.id, created_at), [dog])
        self.assertTrue(True)

    def test_fetch_dogs_3(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account1: Account = create_account(created_at)
        account2: Account = create_account(created_at)
        account1.save()
        account2.save()
        dog1: Dog = create_dog(account1, '1', created_at, 'toto3', BreedType.GERMAN_SHEPHERD)
        dog1.save()
        dog2: Dog = create_dog(account2, '2', created_at, 'toto2', BreedType.GERMAN_SHEPHERD)
        dog2.save()
        dog3: Dog = create_dog(account1, '3', created_at, 'toto1', BreedType.GERMAN_SHEPHERD)
        dog3.save()
        self.assertEqual(fetch_dogs(account1.id, created_at), [dog1, dog3])
