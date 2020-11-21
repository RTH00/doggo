from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def render_privacy_policy(request: HttpRequest) -> HttpResponse:
    return render(request, 'legal/privacy_policy.html')


def render_terms_and_conditions(request: HttpRequest) -> HttpResponse:
    return render(request, 'legal/terms_and_conditions.html')


def render_contact(request: HttpRequest) -> HttpResponse:
    return render(request, 'legal/contact.html')
