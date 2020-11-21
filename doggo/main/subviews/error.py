from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def render_error(request: HttpRequest, error_message: str, error_code: int = 404) -> HttpResponse:
    return render(request, 'error.html', {'error': error_message}, status=error_code)
