from dateutil.tz import UTC
from django.test import TestCase

from main.submodels.account import create_account2, Account
from main.submodels.breed import BreedType
from main.submodels.dog import create_dog, fetch_dog
from main.submodels.events.dog_action_event import add_dog_action_event, DogActionEvent
from main.submodels.events.dog_event import *


class SubmodelsEventsDogActionEventTests(TestCase):

    def setUp(self):
        created_at1: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        created_at2: datetime = datetime(year=2000, month=1, day=2, tzinfo=UTC)
        account1: Account = create_account2('id_secret', created_at1)
        account2: Account = create_account2('id_secret', created_at1)
        account1.save()
        account2.save()
        dog1: Dog = create_dog(account1, 'id_public_1', created_at1, 'toto', BreedType.GOLDEN_RETRIEVER)
        dog2: Dog = create_dog(account2, 'id_public_2', created_at2, 'tata', BreedType.CORGI)
        dog1.save()
        dog2.save()

    def test_add_dog_action_event(self):
        event1: DogActionEvent = add_dog_action_event(
            fetch_dog('id_public_1'),
            fetch_dog('id_public_2'),
            'TEST_CONTEXT',
            'TEST_TYPE',
            datetime(year=2000, month=1, day=3, tzinfo=UTC)
        )
        self.assertNotEqual(event1.id, None)
        self.assertEqual(event1, DogActionEvent.objects.filter(id=event1.id).first())
        self.assertEqual(1, DogActionEvent.objects.count())
        event2: DogActionEvent = add_dog_action_event(
            fetch_dog('id_public_1'),
            None,
            'TEST_CONTEXT',
            'TEST_TYPE',
            datetime(year=2000, month=1, day=3, tzinfo=UTC)
        )
        self.assertNotEqual(event2.id, None)
        self.assertEqual(event2, DogActionEvent.objects.filter(id=event2.id).first())
        self.assertEqual(2, DogActionEvent.objects.count())

    def test_get_last_dog_action_events(self):
        pass  # TODO
