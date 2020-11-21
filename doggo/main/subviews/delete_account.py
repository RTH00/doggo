from django import forms
from django.core.validators import RegexValidator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from main.submodels.account import Account
from main.submodels.dog import Dog
from main.utils.cookie import fetch_account


class CreateDeleteAccountForm(forms.Form):
    dog_name = forms.CharField(
        label='Enter \'DELETE MY ACCOUNT\':',
        max_length=64,
        min_length=1,
        required=True,
        validators=[RegexValidator(
            regex='DELETE MY ACCOUNT',
            message='Enter \'DELETE MY ACCOUNT\', please',
            code='invalid_input'
        )]
    )


def delete_account(account: Account) -> None:
    Dog.objects.filter(account=account).delete()
    account.delete()


@never_cache
@csrf_protect
def render_delete_account(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = CreateDeleteAccountForm(request.POST)
        if form.is_valid():
            delete_account(fetch_account(request))
            return redirect('/')
    else:
        form = CreateDeleteAccountForm()
    return render(request, 'delete_account.html', {
        'form': form
    })
