from datetime import datetime

from dateutil.tz import UTC
from django.http import HttpRequest, HttpResponse
from django.test import TestCase, RequestFactory

from main.submodels.account import Account, create_account2, fetch_account
from main.submodels.dog import create_dog, BreedType, fetch_dog, DogStatus, Dog
from main.submodels.events.dog_action_event import DogActionEvent
from main.submodels.events.dog_action_event_type import DogActionEventType
from main.subviews import dog
from main.subviews.dog import render_dog_action_event, use_magic_bone
from main.utils.cookie import COOKIE_ACCOUNT_ID_SECRET


class SubviewsDogTests(TestCase):

    def setUp(self) -> None:
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('secret_toto', created_at)
        account.save()
        create_dog(account, 'public_dog_id', created_at, 'name', BreedType.GOLDEN_RETRIEVER).save()
        create_dog(account, 'public_dog_id_2', created_at, 'toto', BreedType.GOLDEN_RETRIEVER).save()

    def test_render_dog(self):
        request: HttpRequest = RequestFactory().get('home')
        request.COOKIES[COOKIE_ACCOUNT_ID_SECRET] = 'secret_toto'
        response: HttpResponse = dog.render_dog(request, 'public_dog_id')
        self.assertContains(response, 'name has left.')

    def test_render_dog_action_event_1(self):
        """
        Test tennis ball
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        self.assertEqual(render_dog_action_event(DogActionEvent(
            dog_from=fetch_dog('public_dog_id'),
            dog_to=None,
            context=DogStatus.WALKING,
            type=DogActionEventType.FIND_TENNIS_BALL,
            created_at=created_at
        )),
            '2000-01-01 - While walking, name has found a tennis ball.')

    def test_render_dog_action_event_2(self):
        """
        Test fitness cookie
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        self.assertEqual(render_dog_action_event(DogActionEvent(
            dog_from=fetch_dog('public_dog_id'),
            dog_to=None,
            context=DogStatus.WALKING,
            type=DogActionEventType.FIND_FITNESS_COOKIE,
            created_at=created_at
        )),
            '2000-01-01 - While walking, name has found a fitness cookie.')

    def test_render_dog_action_event_3(self):
        """
        Test magic bone
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        self.assertEqual(render_dog_action_event(DogActionEvent(
            dog_from=fetch_dog('public_dog_id'),
            dog_to=None,
            context=DogStatus.WALKING,
            type=DogActionEventType.FIND_MAGIC_BONE,
            created_at=created_at
        )),
            '2000-01-01 - While walking, name has found a magic bone.')

    def test_render_dog_action_event_4(self):
        """
        Test meet another (left) dog
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        self.assertEqual(render_dog_action_event(DogActionEvent(
            dog_from=fetch_dog('public_dog_id'),
            dog_to=None,
            context=DogStatus.WALKING,
            type=DogActionEventType.MEET_ANOTHER_DOG,
            created_at=created_at
        )),
            '2000-01-01 - While walking, name has met another dog.')

    def test_render_dog_action_event_5(self):
        """
        Test meet another dog
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        self.assertEqual(render_dog_action_event(DogActionEvent(
            dog_from=fetch_dog('public_dog_id'),
            dog_to=fetch_dog('public_dog_id_2'),
            context=DogStatus.WALKING,
            type=DogActionEventType.MEET_ANOTHER_DOG,
            created_at=created_at
        )),
            '2000-01-01 - While walking, name has met <a href="/dog/public_dog_id_2">toto</a>.')

    def test_use_magic_bone_1(self):
        """
        Test use_magic_bone
        :return:
        """
        dog: Dog = fetch_dog('public_dog_id')
        dog.set_status(DogStatus.LEFT, datetime(year=2000, month=1, day=1, tzinfo=UTC))
        dog.save()
        account: Account = fetch_account('secret_toto')
        account.number_magic_bone = 1
        account.save()
        self.assertTrue(use_magic_bone(
            dog,
            account,
            datetime(year=2000, month=1, day=2, tzinfo=UTC)
        ))

    def test_use_magic_bone_2(self):
        """
        Test use_magic_bone
        :return:
        """
        dog: Dog = fetch_dog('public_dog_id')
        dog.set_status(DogStatus.LEFT, datetime(year=2000, month=1, day=1, tzinfo=UTC))
        dog.save()
        account: Account = fetch_account('secret_toto')
        account.number_magic_bone = 0
        account.save()
        self.assertFalse(use_magic_bone(
            dog,
            account,
            datetime(year=2000, month=1, day=2, tzinfo=UTC)
        ))

    def test_use_magic_bone_3(self):
        """
        Test use_magic_bone
        :return:
        """
        dog: Dog = fetch_dog('public_dog_id')
        dog.set_status(DogStatus.AVAILABLE, datetime(year=2000, month=1, day=1, tzinfo=UTC))
        dog.save()
        account: Account = fetch_account('secret_toto')
        account.number_magic_bone = 1
        account.save()
        self.assertFalse(use_magic_bone(
            dog,
            account,
            datetime(year=2000, month=1, day=2, tzinfo=UTC)
        ))
