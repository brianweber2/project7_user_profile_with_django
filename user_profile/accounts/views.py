from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import forms
from . import models

def sign_in(request):
    """User sign-in view."""
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Email or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})

def sign_up(request):
    """User sign-up view."""
    form = forms.UserCreateForm()
    if request.method == 'POST':
        form = forms.UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'accounts/sign_up.html', {'form': form})

def sign_out(request):
    """User sign-out view."""
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))

def user_profile(request, pk):
    """Display user profile information."""
    pass

def edit_user_profile(request, pk):
    """Edit user profile information."""
    pass

def change_password(request):
    """Change a user's password."""
    pass
