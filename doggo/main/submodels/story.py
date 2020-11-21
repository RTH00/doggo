from typing import Optional

from django.db import models

from main.submodels.dog import Dog
from main.utils.story.graph import START_WALK_NODE


class Story(models.Model):
    class Meta:
        db_table = 'stories'

    id = models.BigAutoField(auto_created=True, primary_key=True)
    dog: Dog = models.OneToOneField(Dog, on_delete=models.CASCADE)
    state: str = models.TextField(null=True)


def create_story(dog: Dog) -> Story:
    story: Story = Story(dog=dog, state=START_WALK_NODE)
    story.save()
    return story


def fetch_story(dog: Dog) -> Optional[Story]:
    return Story.objects.filter(dog=dog).first()
