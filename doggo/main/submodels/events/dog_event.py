from typing import Optional, List

from django.db import models
from django.db.models.functions.datetime import datetime

from main.submodels.dog import Dog


class DogEventType:
    ADOPTION = 'ADOPTION'
    LEFT = 'LEFT'


MAX_DOG_EVENT = 20


class DogEvent(models.Model):
    """
    Model to show created/lost dogs in the home page.
    """

    class Meta:
        db_table = 'dog_events'
        indexes = [
            models.Index(fields=['-created_at']),
        ]

    id = models.BigAutoField(auto_created=True, primary_key=True)
    dog: Optional[Dog] = models.ForeignKey(Dog, null=True, on_delete=models.SET_NULL)
    type: str = models.TextField(null=True)
    created_at: datetime = models.DateTimeField(null=True)


def add_dog_event(dog: Dog, type: str, created_at: datetime) -> DogEvent:
    dog_event: DogEvent = DogEvent(dog=dog, type=type, created_at=created_at)
    dog_event.save()
    # delete old
    dog_events: List[DogEvent] = list(DogEvent.objects.order_by('-created_at')[MAX_DOG_EVENT:])
    for dog_event in dog_events:
        dog_event.delete()
    return dog_event


def get_last_dog_events(limit: int) -> List[DogEvent]:
    return list(DogEvent.objects.order_by('-created_at')[:limit])
