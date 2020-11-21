from random import random
from typing import Dict, Callable

from main.submodels.breed import BreedProperties, BREED_PROPERTIES
from main.submodels.dog import *
from main.submodels.events.dog_action_event import add_dog_action_event
from main.submodels.events.dog_action_event_type import DogActionEventType
from main.submodels.story import create_story
from main.utils.token import random_token


def apply_find_magic_bone(dog: Dog, context: str, now: datetime) -> None:
    # account level
    account: Account = dog.account
    account.number_magic_bone = account.number_magic_bone + 1
    account.save()
    # dog action level
    add_dog_action_event(
        dog_from=dog,
        dog_to=None,
        context=context,
        type=DogActionEventType.FIND_MAGIC_BONE,
        created_at=now
    )


def apply_find_fitness_cookie(dog: Dog, context: str, now: datetime) -> None:
    # account level
    account: Account = dog.account
    account.number_fitness_cookie = account.number_fitness_cookie + 1
    account.save()
    # dog action level
    add_dog_action_event(
        dog_from=dog,
        dog_to=None,
        context=context,
        type=DogActionEventType.FIND_FITNESS_COOKIE,
        created_at=now
    )


def apply_find_tennis_ball(dog: Dog, context: str, now: datetime) -> None:
    # account level
    account: Account = dog.account
    account.number_tennis_ball = account.number_tennis_ball + 1
    account.save()
    # dog action level
    add_dog_action_event(
        dog_from=dog,
        dog_to=None,
        context=context,
        type=DogActionEventType.FIND_TENNIS_BALL,
        created_at=now
    )


def apply_meet_another_random_dog(dog: Dog, another_dog: Dog, context: str, now: datetime) -> bool:
    if another_dog is not None and another_dog.id != dog.id:
        add_dog_action_event(
            dog_from=dog,
            dog_to=another_dog,
            context=context,
            type=DogActionEventType.MEET_ANOTHER_DOG,
            created_at=now
        )
        return True
    else:
        return False


def apply_meet_another_dog(dog: Dog, context: str, now: datetime) -> None:
    another_dog = fetch_and_update_random_dog(now)
    apply_meet_another_random_dog(dog, another_dog, context, now)


# TODO test
def apply_go_story(dog: Dog, context: str, now: datetime) -> None:
    create_story(dog)
    add_dog_action_event(
        dog_from=dog,
        dog_to=None,
        context=context,
        type=DogActionEventType.GO_STORY,
        created_at=now
    )


ACTION_APPLIER: Dict[str, Callable[[Dog, str, datetime], None]] = {
    DogActionEventType.FIND_MAGIC_BONE: apply_find_magic_bone,
    DogActionEventType.FIND_FITNESS_COOKIE: apply_find_fitness_cookie,
    DogActionEventType.FIND_TENNIS_BALL: apply_find_tennis_ball,
    DogActionEventType.MEET_ANOTHER_DOG: apply_meet_another_dog,
    DogActionEventType.GO_STORY: apply_go_story
}


def apply_decreasing_rate(value: float, rate: float, last_refresh: datetime, now: datetime) -> float:
    """
    Apply a decreasing rate to a value
    :param value: current value
    :param rate: per second
    :param last_refresh:
    :param now:
    :return: updated value
    """
    diff: float = (now - last_refresh).total_seconds()
    return value - (diff * rate)


def converge(value: float, target: float, ratio: float) -> float:
    diff: float = (target - value) * ratio
    return value + diff


def get_breed_properties(dog: Dog) -> BreedProperties:
    return BREED_PROPERTIES[dog.breed]


def update_nothing(dog: Dog, now: datetime) -> None:
    pass


def apply_action(dog: Dog, action_type: str, context: str, now: datetime):
    ACTION_APPLIER[action_type](dog, context, now)


def random_proba_sample(proba: float) -> bool:
    value: float = random()
    return value < proba


def random_events_sample(events: Dict[str, float], dog: Dog, context: str, now: datetime):
    """
    Apply (or not) a random action
    :param events: event + proba of event
    :param dog: current dog
    :param context: context of the action (Dog.Status)
    :param now: datetime
    :return:
    """
    for action, proba in events.items():
        if random_proba_sample(proba):
            apply_action(dog, action, context, now)


def random_walking_action(dog: Dog, now: datetime):
    random_events_sample(
        get_breed_properties(dog).walking_action_probability,
        dog,
        DogStatus.WALKING,
        now
    )


def update_walking(dog: Dog, now: datetime) -> None:
    if dog.status_set_at + WALKING_TIME <= now:
        dog.set_status(DogStatus.AVAILABLE, now)
        breed_properties: BreedProperties = get_breed_properties(dog)
        dog.fat = converge(dog.fat, 0.0, breed_properties.walking_fat_converge_rate)
        dog.affection = converge(dog.affection, 1.0, breed_properties.walking_affection_converge_rate)
        dog.save()  # save the status to prevent infinite recursion
        random_walking_action(dog, now)


def random_playing_event(dog: Dog, now: datetime):
    random_events_sample(
        get_breed_properties(dog).playing_action_probability,
        dog,
        DogStatus.PLAYING,
        now
    )


def update_playing(dog: Dog, now: datetime) -> None:
    if dog.status_set_at + PLAYING_TIME <= now:
        dog.set_status(DogStatus.AVAILABLE, now)
        breed_properties: BreedProperties = get_breed_properties(dog)
        dog.fat = converge(dog.fat, 0.0, breed_properties.playing_fat_converge_rate)
        dog.affection = converge(dog.affection, 1.0, breed_properties.playing_affection_converge_rate)
        dog.save()  # save the status to prevent infinite recursion
        random_playing_event(dog, now)


def update_eating(dog: Dog, now: datetime) -> None:
    if dog.status_set_at + EATING_TIME <= now:
        dog.set_status(DogStatus.AVAILABLE, now)
        breed_properties: BreedProperties = get_breed_properties(dog)
        dog.food = min(dog.food + breed_properties.eating_food_increase, 1.0)
        dog.fat = min(dog.fat + breed_properties.eating_fat_increase, 1.0)


STATUS_UPDATERS: Dict[str, Callable[[Dog, datetime], None]] = {
    DogStatus.AVAILABLE: update_nothing,
    DogStatus.LEFT: update_nothing,
    DogStatus.WALKING: update_walking,
    DogStatus.EATING: update_eating,
    DogStatus.PLAYING: update_playing
}


def update(dog: Dog, now: datetime) -> None:
    if dog.status == DogStatus.LEFT and dog.status_set_at + LEFT_TIME <= now:
        dog.delete()
    else:
        if dog.status != DogStatus.LEFT:
            breed_properties: BreedProperties = get_breed_properties(dog)
            dog.food = max(
                0.0,
                apply_decreasing_rate(
                    dog.food,
                    breed_properties.food_consumption_rate,
                    dog.last_refresh,
                    now
                )
            )
            dog.affection = max(
                0.0,
                apply_decreasing_rate(
                    dog.affection,
                    breed_properties.affection_consumption_rate,
                    dog.last_refresh,
                    now
                )
            )
            STATUS_UPDATERS[dog.status](dog, now)
            # check is dog has left
            if dog.happiness() <= 0.0:
                dog.set_status(DogStatus.LEFT, now)
            dog.last_refresh = now
            dog.save()


def fetch_and_update_random_dog(now: datetime) -> Optional[Dog]:
    token: str = random_token(30)
    random_dog: Optional[Dog] = fetch_dog_close_id_public(token)
    if random_dog is not None:
        update(random_dog, now)
    return random_dog

