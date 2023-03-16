from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import mail_managers
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

from .decorators import authentication_not_required
from .forms import RegistrationForm, ModifyProfileForm
from .models import User
from .token import token_generator


# Create your views here.
@authentication_not_required
def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.age = form.cleaned_data['age']
            user.terms_and_privacy = form.cleaned_data['terms_and_privacy']
            user.ip = request.META.get('REMOTE_ADDR')
            user.is_active = False
            user.save()
            form.send_activation_email(request, user)
            return redirect('registration:info_account_activation')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags="danger")
    else:
        form = RegistrationForm()
    return render(request, 'accounts/sign-up.html', {'form': form, 'section': 'sign_up'})


@authentication_not_required
def info_account_activation(request):
    return render(request, 'accounts/message_activation_account.html')


@authentication_not_required
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(User, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.email_confirmation = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Your account has been confirmed successfully.',
                             extra_tags='success')
        mail_managers('Un nuovo account e confermato con successo', 'E stato attivato un nuovo account')
        return redirect('login')
    else:
        return render(request, 'accounts/email_activation_invalid.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ModifyProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.first_name = form.cleaned_data['first_name']
            form.last_name = form.cleaned_data['last_name']
            form.age = form.cleaned_data['age']
            form.gender = form.cleaned_data['gender']
            form.city = form.cleaned_data['city']
            form.contry = form.cleaned_data['contry']
            form.avatar = form.cleaned_data['avatar']
            form.ip = request.META.get('REMOTE_ADDR')
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Data updated successfully.')
            return redirect('registration:update_profile')
        else:
            messages.add_message(request, messages.ERROR, 'Please fill in all fields correctly and try again.',
                                 extra_tags='danger')
    else:
        form = ModifyProfileForm(instance=request.user)
    return render(request, 'dashboard/accounts/profile.html', {'form': form, 'section': 'profile'})


@login_required
def delete_user(request):
    user = get_object_or_404(User, is_active=True, username=request.user)
    if request.method == 'POST':
        user.ip = request.META.get('REMOTE_ADDR')
        user.is_active = False
        user.save()
        logout(request)
        messages.add_message(request, messages.ERROR, 'Your account has been successfully deactivated.',
                             extra_tags='danger')
        return redirect('logout')
    else:
        messages.add_message(request, messages.ERROR,
                             'Your account has not been deactivated because a problem has occurred, '
                             'to deactivate it contact us via email.', extra_tags='danger', )
        # mail_managers('Bug - në funksionin delete_user', 'Ka ndodhur dicka e papritur për të çaktivizuar userin')
        return redirect('pages:dashboard')
