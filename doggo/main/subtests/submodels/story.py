from django.test import TestCase
from dateutil.tz import UTC
from main.submodels.account import create_account2, create_account
from main.submodels.dog import *
from main.submodels.story import create_story, fetch_story, Story
from main.utils.story.graph import START_WALK_NODE


class SubmodelsStoryTests(TestCase):

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

    def test_create_story(self):
        dog: Dog = fetch_dog('id_public_1')
        create_story(dog)
        story: Story = fetch_story(dog)
        self.assertEquals(story.state, START_WALK_NODE)
        self.assertEquals(story.dog.id, dog.id)

    def test_fetch_story(self):
        dog: Dog = fetch_dog('id_public_1')
        self.assertIsNone(fetch_story(dog))
        create_story(dog)
        self.assertIsNotNone(fetch_story(dog))
        self.assertIsNone(fetch_story(fetch_dog('id_public_2')))
        fetch_story(dog).delete()
        self.assertIsNone(fetch_story(dog))
