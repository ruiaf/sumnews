from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib import messages

from registration.forms import *

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'])
            user_auth = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user_auth)
            messages.success(request, 'You have registered successfully.')
            return HttpResponseRedirect('/')
        messages.success(request, 'Sorry, we were not able to sign you up.')
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {
        'form': form
    })
 
    return render_to_response('registration/signup.html', variables)
