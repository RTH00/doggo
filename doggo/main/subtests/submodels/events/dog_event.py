from datetime import timedelta
from random import shuffle

from dateutil.tz import UTC
from django.test import TestCase

from main.submodels.account import create_account2, Account
from main.submodels.breed import BreedType
from main.submodels.dog import create_dog
from main.submodels.events.dog_event import *


class SubmodelsEventsDogEventTests(TestCase):

    def test_create_account(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, 'id_public', created_at, 'toto', BreedType.CHICKEN)
        dog.save()
        indexes: List[int] = list(range(0, 100))
        shuffle(indexes)
        for i in indexes:
            add_dog_event(dog, DogEventType.ADOPTION, created_at + timedelta(seconds=i))
        self.assertEqual(20, len(DogEvent.objects.all()))
        dog_events: List[DogEvent] = get_last_dog_events(3)
        self.assertEqual('2000-01-01 00:01:39+00:00', str(dog_events[0].created_at))
        self.assertEqual('2000-01-01 00:01:38+00:00', str(dog_events[1].created_at))
        self.assertEqual('2000-01-01 00:01:37+00:00', str(dog_events[2].created_at))


# test with dog in dog_event None
