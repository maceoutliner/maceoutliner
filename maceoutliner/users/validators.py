from registration.validators import ReservedNameValidator, validate_confusables, validate_confusables_email

custom_validators = [validate_confusables, validate_confusables_email, ReservedNameValidator()]
