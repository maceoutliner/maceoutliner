from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from registration.validators import ReservedNameValidator, validate_confusables, validate_confusables_email
from .models import User


def validate_usernames_icase(value):
    '''
    Takes the proposed username, and verifies that there is not already a case-insensitive match
    in the database.
    '''
    matches = User.objects.filter(username__iexact=value)
    if matches:
        raise ValidationError(_('This username is already taken. Please select another.'))


custom_validators = [validate_usernames_icase, validate_confusables,
                     validate_confusables_email, ReservedNameValidator()]
