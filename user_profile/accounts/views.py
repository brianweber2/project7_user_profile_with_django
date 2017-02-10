from django.contrib import messages
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

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
                    messages.success(request, "You've been logged in.")
                    return HttpResponseRedirect(reverse('accounts:profile'))
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
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/sign_up.html', {'form': form})

@login_required
def sign_out(request):
    """User sign-out view."""
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))

@login_required
def user_profile(request):
    """Display user profile information."""
    user = request.user
    return render(request, 'accounts/profile.html', {'user': user})

@login_required
def edit_user_profile(request):
    """Edit user profile information."""
    user = request.user
    form1 = forms.UserUpdateForm(instance=user)
    form2 = forms.UserProfileUpdateForm(instance=user.userprofile)
    if request.method == 'POST':
        form1 = forms.UserUpdateForm(instance=user, data=request.POST)
        form2 = forms.UserProfileUpdateForm(
            instance=user.userprofile,
            data=request.POST,
            files=request.FILES
        )
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, "Your profile has been updated!")
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/edit_profile.html',
        {'form1': form1, 'form2': form2})

@login_required
def change_password(request):
    """Change a user's password."""
    form = forms.ValidatingPasswordChangeForm(
        user=request.user,
        request=request
    )
    if request.method == 'POST':
        form = forms.ValidatingPasswordChangeForm(
            user=request.user,
            data=request.POST,
            request=request
        )
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been updated!")
            return HttpResponseRedirect(reverse('accounts:profile'))
    return render(request, 'accounts/change_password.html', {'form': form})
