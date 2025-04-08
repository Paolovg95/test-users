from django.shortcuts import render,redirect
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse
# ALL AUTH
from allauth.account.models import EmailAddress, EmailConfirmation, EmailConfirmationHMAC
from allauth.account.forms import LoginForm
from allauth.account.utils import send_email_confirmation
# ACCOUNTS APP
from .models import Invitation
from .forms import CustomSignupForm, CompanyForm, SendInviteForm, UserProfileForm

#  COMPANY INVITATIONS
def create_invitation(request, company):
    if request.method == "GET":
        create_invitation_form = SendInviteForm()
        return render(request, 'invitations/invitations.html', {'create_invitation_form': create_invitation_form, 'company': company})
    if request.method == "POST":
        user = request.user
        send_invitaton_form = SendInviteForm(request.POST)
        if send_invitaton_form.is_valid():
            key = get_random_string(64).lower()
            email = send_invitaton_form.cleaned_data['email']
            invitation = Invitation.objects.create(email=email, key=key, inviter=user)
            url = f"http://localhost:8000/company-invitation/?token={key}"
            message = EmailMessage(to=["paolo9517@gmail.com"], subject="Testing Invite Mailgun" ,body=f"Go to this link to accept the invite: {url}")
            message.send()
            return render(request, 'invite_confirmation.html', {'email': email})
def accept_invitation(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        invite = Invitation.objects.get(key=token)
        if invite.accepted:
            return render(request, 'invitations/invite_expired.html', {})
        else:
            company = invite.inviter.userprofile.company
            user_form = CustomSignupForm()
            profile_form = UserProfileForm()
            company_form = CompanyForm()
            return render(request, "invitations/accept_invite.html", {"invite": invite, "company": company, 'user_form': user_form, 'profile_form': profile_form, 'company_form': company_form})
    if request.method == "POST":
        token = request.POST.get('token')
        invite = Invitation.objects.get(key=token)
        user_form = CustomSignupForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            company = invite.inviter.company
            user.save()
            profile.user = user
            profile.company = company
            profile.save()
            invite.accepted = True
            invite.save()
            message = EmailMessage(to=["paolo9517@gmail.com"], subject="Testing Sign Up Mailgun" ,body=f"Go to this link to accept the invite: ...")
            message.send()
            return HttpResponse("Saved from Invite!")
        else:
            return HttpResponse("Form not valid!")


# USER AUTHENTICATION CONFIRMATION - W/O ALL-AUTH
def signup(request):
    if request.method == "GET":
        signup_form = CustomSignupForm()
        return render(request, "accounts/signup.html", {'signup_form': signup_form})
    if request.method == "POST":
        signup_form = CustomSignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            email_address = EmailAddress.objects.create(user=user, email= user.email, verified=False, primary=False)
            send_email_confirmation(request, user, signup=True, email=user.email)
            return redirect('account_email_verification_sent')
# def login(request):
#     if request.method == "GET":
#         login_form = LoginForm()
#         return render(request, "accounts/login.html", {'login_form': login_form })
# def email_confirmation(request, key):
#     if request.method == "GET":
#         return render(request, 'accounts/email_confirmation.html', {})

    # if request.method == "GET":
    #     if key is not None:
    #         confirmation = EmailConfirmation.objects.get(key=key)
    #         if confirmation:
    #             if confirmation.verified == False:
    #                 return render(request, 'accounts/email_confirmation.html', {'confirmation': confirmation, 'can_confirm': True})
    #             else:
    #                 return render(request, 'accounts/email_confirmation.html', {'confirmation': confirmation, 'can_confirm': False})
    #         else:
    #             return render(request, 'accounts/email_confirmation.html', {})
    #     else:
    #         return redirect('email_confirmation_url')
    # if request.method == "POST":
    #     if key is not None:


@login_required
def account_view(request):
    user = request.user
    company = user.company.name
    return render(request, 'home.html', {'company': company, 'user': user})
