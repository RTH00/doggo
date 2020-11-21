from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


@never_cache
@csrf_protect
def render_index(request: HttpRequest) -> HttpResponse:
    return redirect('home')
