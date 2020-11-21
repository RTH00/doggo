from datetime import datetime
from typing import Optional, List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.cache import never_cache

from main.submodels.dog import Dog
from main.submodels.dog_updater import fetch_and_update_random_dog
from main.submodels.events.dog_event import get_last_dog_events, DogEvent, DogEventType
from main.subviews.dogs import fetch_dogs
from main.utils import cookie
from main.submodels.account import Account


ANNOUNCEMENTS = [
    'Updated Doggo characteristics!',
    'Bug fixes',
    'Doggo is now secure! You can use https!',
    'Go to your account to get a link to share your account between multiple devices!',
    'More stories!',
]


@never_cache
def render_home(request: HttpRequest) -> HttpResponse:
    now: datetime = timezone.now()
    # process random dog
    random_dog: Optional[Dog] = fetch_and_update_random_dog(now)
    # process can create dog
    account: Account = cookie.fetch_account(request)
    dogs: List[Dog] = fetch_dogs(account.id, now)
    # process last events
    dog_events: List[DogEvent] = get_last_dog_events(5)
    return render(request, 'home.html', context={
        'random_dog': random_dog,
        'has_no_dog': len(dogs) == 0,
        'announcements': ANNOUNCEMENTS,
        'DogEventType': DogEventType,
        'dog_events': dog_events
    })
