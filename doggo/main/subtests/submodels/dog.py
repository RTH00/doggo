from dateutil.tz import UTC
from django.test import TestCase

from main.submodels.account import create_account2, create_account
from main.submodels.dog import *


class SubmodelsDogTests(TestCase):

    def test_age(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        self.assertEqual(0, dog.age(datetime(year=1999, month=1, day=1, tzinfo=UTC)))
        self.assertEqual(0, dog.age(datetime(year=2000, month=1, day=1, hour=1, tzinfo=UTC)))
        self.assertEqual(2, dog.age(datetime(year=2000, month=1, day=3, tzinfo=UTC)))

    def test_create_dog(self):
        """
        Check all fields are setup correctly with create_dog(...)
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GOLDEN_RETRIEVER)
        self.assertEqual('id_public', dog.id_public)
        self.assertEqual(created_at, dog.created_at)
        self.assertEqual('name', dog.name)
        self.assertEqual(BreedType.GOLDEN_RETRIEVER, dog.breed)

    def test_fetch_dogs_5(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account(created_at)
        account.save()
        # no dogs
        self.assertIsNone(fetch_dog_close_id_public(''))
        # add dogs
        create_dog(account, '1', created_at, 'name', BreedType.GERMAN_SHEPHERD).save()
        create_dog(account, '2', created_at, 'name', BreedType.GERMAN_SHEPHERD).save()
        create_dog(account, '4', created_at, 'name', BreedType.GERMAN_SHEPHERD).save()
        self.assertEqual('2', fetch_dog_close_id_public('2').id_public)
        self.assertEqual('1', fetch_dog_close_id_public('0').id_public)
        self.assertEqual('4', fetch_dog_close_id_public('3').id_public)
        self.assertEqual('4', fetch_dog_close_id_public('9').id_public)
