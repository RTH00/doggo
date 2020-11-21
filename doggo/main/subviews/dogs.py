from datetime import datetime
from typing import List

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect

from main.submodels import dog_updater
from main.submodels.account import Account
from main.submodels.dog import Dog
from main.utils.cookie import fetch_account

MAX_NUMBER_OF_DOGS: int = 3


def fetch_dogs(account_id: int, now: datetime, update: bool = True) -> List[Dog]:
    from main.submodels.dog import Dog
    dogs: List[Dog] = list(Dog.objects.filter(account=account_id).order_by('created_at'))
    if update:
        for dog in dogs:
            dog_updater.update(dog, now)
    return dogs


@csrf_protect
def render_dogs(request: HttpRequest) -> HttpResponse:
    # check there is at least one dog alive or switch to create_dog
    now: datetime = timezone.now()
    account: Account = fetch_account(request)
    dogs: List[Dog] = fetch_dogs(account.id, now)
    if len(dogs) == 0:
        return redirect('create_dog')
    else:
        return render(request, 'dogs.html', context={
            'account': account,
            'dogs': dogs,
            'can_create_dog': len(dogs) < MAX_NUMBER_OF_DOGS,
        })
