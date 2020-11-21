from random import randrange

from django import forms
from django.core.validators import RegexValidator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from main.submodels.dog import *
from main.submodels.events.dog_event import add_dog_event, DogEventType
from main.subviews.dogs import fetch_dogs
from main.utils.cookie import fetch_account
from main.utils.token import random_token

MAX_NUMBER_OF_DOGS: int = 3


class CreateDogForm(forms.Form):
    dog_name = forms.CharField(
        label='Dog name:',
        max_length=32,
        min_length=1,
        validators=[RegexValidator(r'^[0-9a-zA-Z ]*$', 'Only alphanumeric characters and spaces are allowed.')]
    )
    dog_breed = forms.ChoiceField(
        label='Breed:',
        choices=[
            (BreedType.GOLDEN_RETRIEVER, 'Golden Retriever'),
            (BreedType.GERMAN_SHEPHERD, 'German Shepherd'),
            (BreedType.CORGI, 'Corgi'),
            (BreedType.CHICKEN, 'Chicken')
        ])


@never_cache
@csrf_protect
def render_create_dog(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateDogForm(request.POST)
        if form.is_valid():
            now: datetime = timezone.now()
            account: Account = fetch_account(request)
            if len(fetch_dogs(account.id, now)) < MAX_NUMBER_OF_DOGS:
                id_public: str = random_token(30)
                dog: Dog = create_dog(
                    account=account,
                    id_public=id_public,
                    created_at=now,
                    name=form.cleaned_data['dog_name'],
                    breed=form.cleaned_data['dog_breed']
                )
                dog.save()
                add_dog_event(dog, DogEventType.ADOPTION, now)
                return redirect(reverse('dogs'))
            else:
                return render(request, 'error.html', {'error': 'You already have ' + str(MAX_NUMBER_OF_DOGS) + ' dogs!'})
    else:
        form = CreateDogForm()
    return render(request, 'create_dog.html', {
        'form': form,
        'dog_random_image': 'index/dog_' + str(randrange(5)) + '.jpg'
    })
