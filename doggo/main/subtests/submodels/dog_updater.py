from dateutil.tz import UTC
from django.test import TestCase

from main.submodels.account import create_account2, fetch_account
from main.submodels.dog_updater import *
from main.submodels.events.dog_action_event import DogActionEvent, get_last_dog_action_events
from main.subviews.dog import play_dog, walk_dog


class SubmodelsDogUpdaterTests(TestCase):

    def test_apply_decreasing_rate_1(self):
        last_refresh: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        now: datetime = datetime(year=2000, month=1, day=1, second=1, tzinfo=UTC)
        self.assertEqual(0.7, apply_decreasing_rate(1.0, 0.3, last_refresh, now))

    def test_apply_decreasing_rate_2(self):
        last_refresh: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        now: datetime = datetime(year=2000, month=1, day=1, second=1, microsecond=500000, tzinfo=UTC)
        self.assertEqual(0.55, apply_decreasing_rate(1.0, 0.3, last_refresh, now))

    def test_converge_1(self):
        self.assertEqual(0.7, converge(1.0, 0.0, 0.3))

    def test_converge_2(self):
        self.assertEqual(0.3, converge(0.0, 1.0, 0.3))

    def test_converge_3(self):
        self.assertEqual(0.494, converge(0.5, 0.44, 0.1))

    def test_update_available(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.affection = 0.5
        dog.food = 0.5
        dog.status = DogStatus.AVAILABLE
        update(dog, datetime(year=2000, month=1, day=1, hour=1, tzinfo=UTC))
        dog_db: Dog = fetch_dog('id_public')
        self.assertEqual(0.48, dog_db.food)
        self.assertEqual(0.4875, dog_db.affection)

    def test_update_left_1(self):
        """
        Check that a dog with LEFT status is not deleted immediately
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.set_status(DogStatus.LEFT, created_at)
        dog.save()
        update(dog, created_at)
        self.assertIsNotNone(Dog.objects.filter(id=dog.id).first())

    def test_update_left_2(self):
        """
        Check that a dog with LEFT status is deleted after some time
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.set_status(DogStatus.LEFT, created_at)
        dog.save()
        update(dog, created_at + LEFT_TIME + timedelta(seconds=1))
        self.assertIsNone(Dog.objects.filter(id=dog.id).first())

    # TODO move to subviews tests
    def test_update_play(self):
        """
        Check playing state update
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.fat = 0.5
        dog.affection = 0.5
        play_dog(dog, account, created_at)
        update(dog, created_at + PLAYING_TIME + timedelta(seconds=1))
        dog_db: Dog = fetch_dog('id_public')
        self.assertEqual(DogStatus.AVAILABLE, dog_db.status)
        self.assertEqual(0.45, dog_db.fat)
        self.assertEqual(0.5993305555555556, dog_db.affection)

    # TODO move to subviews tests
    def test_update_walk(self):
        """
        Check walking state update
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog1: Dog = create_dog(account, "id_public_1", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog2: Dog = create_dog(account, "id_public_2", created_at, 'name', BreedType.GOLDEN_RETRIEVER)
        dog1.fat = 0.5
        dog1.affection = 0.5
        walk_dog(dog1, account, created_at)
        update(dog1, created_at + WALKING_TIME + timedelta(seconds=1))
        dog2.fat = 0.5
        dog2.affection = 0.5
        walk_dog(dog2, account, created_at)
        update(dog2, created_at + WALKING_TIME + timedelta(seconds=1))
        dog1_db: Dog = fetch_dog('id_public_1')
        dog2_db: Dog = fetch_dog('id_public_2')
        self.assertEqual(DogStatus.AVAILABLE, dog1_db.status)
        self.assertEqual(0.4, dog1_db.fat)
        self.assertEqual(0.6981229166666667, dog1_db.affection)
        self.assertEqual(DogStatus.AVAILABLE, dog2_db.status)
        self.assertEqual(0.35, dog2_db.fat)
        self.assertEqual(0.6478100694444444, dog2_db.affection)

    def test_update_last_refresh(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.save()
        self.assertEqual(created_at, fetch_dog('id_public').last_refresh)
        updated_at_1: datetime = datetime(year=2000, month=1, day=1, minute=1, tzinfo=UTC)
        update(dog, updated_at_1)
        self.assertEqual(updated_at_1, fetch_dog('id_public').last_refresh)
        updated_at_2: datetime = datetime(year=2000, month=1, day=1, minute=1, tzinfo=UTC)
        update(dog, updated_at_2)
        self.assertEqual(updated_at_2, fetch_dog('id_public').last_refresh)

    def test_random_proba_sample(self):
        self.assertTrue(random_proba_sample(1.0))
        self.assertFalse(random_proba_sample(0.0))

    def test_apply_action_find_magic_bone(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.save()
        apply_action(dog, DogActionEventType.FIND_MAGIC_BONE, DogStatus.WALKING, created_at)
        self.assertEqual(2, fetch_account('id_secret').number_magic_bone)
        self.assertEqual(get_last_dog_action_events(fetch_dog('id_public')),
                         [DogActionEvent(
                             id=2,
                             dog_from=dog,
                             dog_to=None,
                             context=DogStatus.WALKING,
                             type=DogActionEventType.FIND_MAGIC_BONE,
                             created_at=created_at
                         )])

    def test_apply_action_find_fitness_cookie(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.save()
        apply_action(dog, DogActionEventType.FIND_FITNESS_COOKIE, DogStatus.PLAYING, created_at)
        self.assertEqual(2, fetch_account('id_secret').number_fitness_cookie)
        self.assertEqual(get_last_dog_action_events(fetch_dog('id_public')),
                         [DogActionEvent(
                             id=1,
                             dog_from=dog,
                             dog_to=None,
                             context=DogStatus.PLAYING,
                             type=DogActionEventType.FIND_FITNESS_COOKIE,
                             created_at=created_at
                         )])

    def test_apply_action_find_tennis_ball(self):
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.save()
        apply_action(dog, DogActionEventType.FIND_TENNIS_BALL, DogStatus.EATING, created_at)
        self.assertEqual(2, fetch_account('id_secret').number_tennis_ball)
        self.assertEqual(get_last_dog_action_events(fetch_dog('id_public')),
                         [DogActionEvent(
                             id=3,
                             dog_from=dog,
                             dog_to=None,
                             context=DogStatus.EATING,
                             type=DogActionEventType.FIND_TENNIS_BALL,
                             created_at=created_at
                         )])

    def test_apply_action_meet_another_dog(self):
        """
        With only 1 dog
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        dog: Dog = create_dog(account, "id_public", created_at, 'name', BreedType.GERMAN_SHEPHERD)
        dog.save()
        apply_action(dog, DogActionEventType.MEET_ANOTHER_DOG, DogStatus.WALKING, created_at)
        self.assertEqual(get_last_dog_action_events(fetch_dog('id_public')), [])

    def test_apply_meet_random_another_dog_1(self):
        """
        With another valid dog
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        create_dog(account, "id_public_1", created_at, 'name_1', BreedType.GERMAN_SHEPHERD).save()
        create_dog(account, "id_public_2", created_at, 'name_2', BreedType.GERMAN_SHEPHERD).save()
        self.assertTrue(apply_meet_another_random_dog(
            fetch_dog('id_public_1'),
            fetch_dog('id_public_2'),
            DogStatus.WALKING,
            created_at)
        )
        self.assertEqual(get_last_dog_action_events(fetch_dog('id_public_1')), [DogActionEvent(
            id=4,
            dog_from=fetch_dog('id_public_1'),
            dog_to=fetch_dog('id_public_2'),
            context=DogStatus.WALKING,
            type=DogActionEventType.MEET_ANOTHER_DOG,
            created_at=created_at
        )])

    def test_apply_meet_random_another_dog_2(self):
        """
        With the same dog
        :return:
        """
        created_at: datetime = datetime(year=2000, month=1, day=1, tzinfo=UTC)
        account: Account = create_account2('id_secret', created_at)
        account.save()
        create_dog(account, "id_public_1", created_at, 'name_1', BreedType.GERMAN_SHEPHERD).save()
        self.assertFalse(apply_meet_another_random_dog(
            fetch_dog('id_public_1'),
            fetch_dog('id_public_1'),
            DogStatus.WALKING,
            created_at)
        )
        self.assertEqual(get_last_dog_action_events(fetch_dog('id_public')), [])
