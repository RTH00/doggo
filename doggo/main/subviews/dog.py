from datetime import datetime
from typing import Callable, Optional, List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from main.submodels import dog_updater
from main.submodels.account import Account
from main.submodels.dog import Dog, fetch_dog, DogStatus, DEFAULT_FOOD, DEFAULT_FAT, DEFAULT_AFFECTION
from main.submodels.events.dog_action_event import DogActionEvent, get_last_dog_action_events
from main.submodels.events.dog_action_event_type import DogActionEventType
from main.submodels.story import Story, fetch_story
from main.subviews.dogs import fetch_dogs
from main.subviews.story import display_story
from main.utils.cookie import fetch_account


def fetch_update_dog(request: HttpRequest,
                     id_public: str,
                     updater: Optional[Callable[[Dog, Account, datetime], bool]]
                     ) -> HttpResponse:
    now: datetime = timezone.now()
    dog: Optional[Dog] = fetch_dog(id_public)
    if dog is not None:
        dog_updater.update(dog, now)
        account: Account = fetch_account(request)
        if updater is not None:
            # TODO redirect to error page if the updater returns false (and test)
            updater(dog, account, now)
        if updater is None:
            return display_dog(request, dog, account, now)
        else:
            return redirect(reverse('dog', kwargs={'id': dog.id_public}))
    else:
        return render(request, 'dog_not_found.html', status=404)


def list_get_or_none(list: List, index: int) -> Optional:
    if 0 <= index < len(list):
        return list[index]
    else:
        return None


# TODO put this in a template
def render_dog_action_event(event: DogActionEvent) -> str:
    message: str = event.created_at.strftime('%Y-%m-%d') + ' - '
    message += 'While ' + event.context.lower() + ', ' + event.dog_from.name
    if event.type == DogActionEventType.FIND_MAGIC_BONE:
        message += ' has found a magic bone.'
    elif event.type == DogActionEventType.FIND_FITNESS_COOKIE:
        message += ' has found a fitness cookie.'
    elif event.type == DogActionEventType.FIND_TENNIS_BALL:
        message += ' has found a tennis ball.'
    elif event.type == DogActionEventType.MEET_ANOTHER_DOG:
        if event.dog_to is None:
            message += ' has met another dog.'
        else:
            message += ' has met <a href="' +\
                       reverse('dog', kwargs={'id': event.dog_to.id_public}) +\
                       '">' + event.dog_to.name + '</a>.'
    elif event.type == DogActionEventType.GO_STORY:
        message += ' has lived an adventure!'
    else:
        raise Exception('Invalid DogActionEventType: ' + event.type)
    return message


def display_dog(request: HttpRequest, dog: Dog, account: Account, now: datetime) -> HttpResponse:
    left_dog: Optional[Dog] = None
    right_dog: Optional[Dog] = None
    is_current_owner: bool = dog.is_owner(account)
    if is_current_owner:
        story: Optional[Story] = fetch_story(dog=dog)
        if story is None:
            dogs: List[Dog] = fetch_dogs(account.id, now, False)
            current_dog_index: int = dogs.index(dog)
            left_dog = list_get_or_none(dogs, current_dog_index - 1)
            right_dog = list_get_or_none(dogs, current_dog_index + 1)
        else:
            return display_story(request, dog, account, story)
    dog_action_events: List[DogActionEvent] = get_last_dog_action_events(dog)
    return render(request, 'dog.html', context={
        'account': account,
        'dog': dog,
        'dog_age': dog.age(now),
        'DogStatus': DogStatus,
        'is_current_owner': is_current_owner,
        'extended_description_status': dog.extended_description_status(now),
        'left_dog': left_dog,
        'right_dog': right_dog,
        'formatted_dog_action_events': list(map(render_dog_action_event, dog_action_events))
    })


def action_allowed(dog: Dog, account: Account) -> bool:
    return dog.status == DogStatus.AVAILABLE and dog.is_owner(account) and fetch_story(dog) is None


# todo move in dog_updater
def feed_dog(dog: Dog, account: Account, now: datetime) -> bool:
    if action_allowed(dog, account):
        dog.set_status(DogStatus.EATING, now)
        dog.save()
        return True
    else:
        return False


# todo move in dog_updater
def walk_dog(dog: Dog, account: Account, now: datetime) -> bool:
    if action_allowed(dog, account):
        dog.set_status(DogStatus.WALKING, now)
        dog.save()
        return True
    else:
        return False


# todo move in dog_updater
def play_dog(dog: Dog, account: Account, now: datetime) -> bool:
    if action_allowed(dog, account):
        dog.set_status(DogStatus.PLAYING, now)
        dog.save()
        return True
    else:
        return False


def use_magic_bone(dog: Dog, account: Account, now: datetime) -> bool:
    if dog.status == DogStatus.LEFT and dog.is_owner(account) and account.number_magic_bone >= 1:
        # reset dog
        dog.set_status(DogStatus.AVAILABLE, now)
        dog.food = DEFAULT_FOOD
        dog.fat = DEFAULT_FAT
        dog.affection = DEFAULT_AFFECTION
        # remove one magic bone
        account.number_magic_bone = account.number_magic_bone - 1
        # save all
        dog.save()
        account.save()
        return True
    else:
        return False


def use_fitness_cookie(dog: Dog, account: Account, now: datetime) -> bool:
    if action_allowed(dog, account) and account.number_fitness_cookie >= 1:
        # remove fat
        dog.fat = 0
        # remove one fitness cookie
        account.number_fitness_cookie = account.number_fitness_cookie - 1
        # save all
        dog.save()
        account.save()
        return True
    else:
        return False


def use_tennis_ball(dog: Dog, account: Account, now: datetime) -> bool:
    if action_allowed(dog, account) and account.number_tennis_ball >= 1:
        # add affection
        dog.affection = 1.0
        # remove one fitness cookie
        account.number_tennis_ball = account.number_tennis_ball - 1
        # save all
        dog.save()
        account.save()
        return True
    else:
        return False


@never_cache
@csrf_protect
def render_dog(request: HttpRequest, id: str = '') -> HttpResponse:
    return fetch_update_dog(request, id, None)


@never_cache
@csrf_protect
def render_feed_dog(request: HttpRequest, id: str = '') -> HttpResponse:
    return fetch_update_dog(request, id, feed_dog)


@never_cache
@csrf_protect
def render_walk_dog(request: HttpRequest, id: str = '') -> HttpResponse:
    return fetch_update_dog(request, id, walk_dog)


@never_cache
@csrf_protect
def render_play_dog(request: HttpRequest, id: str = '') -> HttpResponse:
    return fetch_update_dog(request, id, play_dog)


@never_cache
@csrf_protect
def render_use_magic_bone(request: HttpRequest, id: str = '') -> HttpResponse:
    return fetch_update_dog(request, id, use_magic_bone)


@never_cache
@csrf_protect
def render_use_fitness_cookie(request: HttpRequest, id: str = '') -> HttpResponse:
    return fetch_update_dog(request, id, use_fitness_cookie)


@never_cache
@csrf_protect
def render_use_tennis_ball(request: HttpRequest, id: str = '') -> HttpResponse:
    return fetch_update_dog(request, id, use_tennis_ball)
