from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .models import StaffWhitelist, Profile


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user_email = sociallogin.user.email
        if sociallogin.is_existing:
            return
        try:
            existing_user = User.objects.get(email__iexact=user_email)
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            pass

        email_domain = user_email.split("@")[-1]

        if email_domain == "pilani.bits-pilani.ac.in":
            sociallogin.account.extra_data["role"] = Profile.Role.STUDENT
        else:
            try:
                whitelist_entry = StaffWhitelist.objects.get(
                    profile__user__email=user_email
                )
                sociallogin.account.extra_data["role"] = Profile.Role.STAFF
            except StaffWhitelist.DoesNotExist:
                raise ImmediateHttpResponse(
                    HttpResponseForbidden(
                        "Access Denied: Your email is not authorized."
                    )
                )

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        try:
            role = sociallogin.account.extra_data.get("role")
            if role:
                Profile.objects.update_or_create(user=user, defaults={"role": role})
        except Exception as e:
            print(f"Error creating profile for {user.email}: {e}")

        return user
