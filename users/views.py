from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import re


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, f'Account created. Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
    # if request.method == 'POST':
    #     form = UserRegisterForm(request.POST)
    #     p_form = ProfileUpdateForm(request.POST)
    #     if form.is_valid() and p_form.is_valid():
    #         form.save()
    #         p_form.save()
    #         # username = form.cleaned_data.get('username')
    #         messages.success(request, f'Account created. Please login.')
    #         return redirect('login')
    # else:
    #     form = UserRegisterForm()
    #     p_form = ProfileUpdateForm()
    # return render(request, 'users/register.html', {'form': form, 'p_form': p_form})


def is_valid_us_phone_number(phone_number):
    """
    Validates a US phone number.

    Args:
    phone_number: The phone number to validate.

    Returns:
    True if the phone number is valid, False otherwise.
    """

    # The regular expression to match a valid US phone number.
    regex = re.compile(r'^\d{10}$|^\d{3}-\d{3}-\d{4}$')

    # Check if the phone number matches the regular expression.
    if regex.match(phone_number):
        return True
    else:
        return False


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account profile has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)
