from datetime import datetime
from random import random, shuffle
from typing import Optional, Tuple

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from main.submodels.account import Account
from main.submodels.dog import Dog, fetch_dog
from main.submodels.story import Story, fetch_story
from main.subviews.error import render_error
from main.utils.cookie import fetch_account
from main.utils.story.graph import STORY_GRAPH
from main.utils.story.node import Node, NodeLink, sample_node_links, find_choice, Choice


def display_story(request: HttpRequest, dog: Dog, account: Account, story: Story) -> HttpResponse:
    """
    Must be call only by the owner
    :param request:
    :param dog:
    :param account:
    :param story:
    :return:
    """
    story_node: Node = STORY_GRAPH[story.state]
    choices: [Tuple[str, str]] = []
    for choice in story_node.choices:
        choices.append((choice.text(dog), choice.id))
    # randomise choices order
    shuffle(choices)
    return render(request, 'story.html', context={
        'dog': dog,
        'account': account,
        'story_text': story_node.text(dog),
        'choices': choices
    })


def apply_story_choice(story: Story, choice_id: str, account: Account, dog: Dog) -> None:
    node: Optional[Node] = STORY_GRAPH.get(story.state)
    if node is None:
        story.delete()
    else:
        choice: Optional[Choice] = find_choice(choice_id, node.choices)
        if choice is None:
            return None
        next_node_id: str = sample_node_links(choice.links)
        next_node: Node = STORY_GRAPH.get(next_node_id)
        if next_node is None:
            story.delete()
        else:
            next_node.effect(account, dog)
            story.state = next_node_id
            story.save()


@never_cache
@csrf_protect
def render_cancel_story(request: HttpRequest, dog_id: str = '') -> HttpResponse:
    account: Optional[Account] = fetch_account(request)
    dog: Optional[Dog] = fetch_dog(dog_id)
    if account is None:
        return render_error(request, "Account not found.")
    if dog is None:
        return render_error(request, "Dog not found.")
    if not dog.is_owner(account):
        return render_error(request, "This doggo is not yours!")
    story: Optional[Story] = fetch_story(dog)
    if story is None:
        return render_error(request, "Story not found.")
    story.delete()
    return redirect(reverse('dog', kwargs={'id': dog.id_public}))


@never_cache
@csrf_protect
def render_story_choice(request: HttpRequest, dog_id: str = '', choice_id: str = '') -> HttpResponse:
    """
    TODO add security check that the account is the owner
    :param request:
    :param dog_id:
    :param choice_id:
    :return:
    """
    account: Optional[Account] = fetch_account(request)
    dog: Optional[Dog] = fetch_dog(dog_id)
    if account is None:
        return render_error(request, "Account not found.")
    if dog is None:
        return render_error(request, "Dog not found.")
    if not dog.is_owner(account):
        return render_error(request, "This doggo is not yours!")
    story: Optional[Story] = fetch_story(dog)
    if story is None:
        return render_error(request, "Story not found.")
    apply_story_choice(story, choice_id, account, dog)
    return redirect(reverse('dog', kwargs={'id': dog.id_public}))
