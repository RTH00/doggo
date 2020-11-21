from datetime import datetime
from typing import Optional, List

from django.db import models

from main.submodels.dog import Dog


MAX_DOG_ACTION_EVENT = 5  # per dog

# TODO add tests to check that all the events related to a dog are deleted when the dog is deleted


class DogActionEvent(models.Model):
    class Meta:
        db_table = 'dog_action_events'
        indexes = [
            models.Index(fields=['dog_from', '-created_at']),
        ]

    id = models.BigAutoField(auto_created=True, primary_key=True)
    dog_from: Dog = models.ForeignKey(Dog, related_name='dog_from', null=True, on_delete=models.CASCADE)
    dog_to: Optional[Dog] = models.ForeignKey(Dog, related_name='dog_to', null=True, on_delete=models.SET_NULL)
    context: str = models.TextField(null=True)
    type: str = models.TextField(null=True)
    created_at: datetime = models.DateTimeField(null=True)


def add_dog_action_event(dog_from: Dog,
                         dog_to: Optional[Dog],
                         context: str,
                         type: str,
                         created_at: datetime
                         ) -> DogActionEvent:
    ret: DogActionEvent = DogActionEvent(
        dog_from=dog_from,
        dog_to=dog_to,
        context=context,
        type=type,
        created_at=created_at
    )
    ret.save()
    # delete old
    dog_action_events: List[DogActionEvent] =\
        list(DogActionEvent.objects.filter(dog_from=dog_from).order_by('-created_at')[MAX_DOG_ACTION_EVENT:])
    for dog_action_event in dog_action_events:
        dog_action_event.delete()
    return ret


def get_last_dog_action_events(dog: Dog) -> List[DogActionEvent]:
    return list(DogActionEvent.objects.filter(dog_from=dog).order_by('-created_at'))
