import logging
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


logger = logging.getLogger('users')


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        logger.debug('Request for account adapter ready for signup.')
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def save_user(self, request, user, form, commit=True):
        display_name = form.cleaned_data.get('display_name')
        logger.debug('Found requested display_name of {0} for {1}'.format(display_name, form.cleaned_data['username']))
        if display_name:
            logger.debug('Attempting to save to model field.')
            user_field(user, 'display_name', display_name)
        return super().save_user(request, user, form, commit)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_SOCIAL_REGISTRATION', True)  # pragma: no cover We don't use this.
