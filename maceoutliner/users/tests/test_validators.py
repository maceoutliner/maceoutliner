import pytest
from django.core.exceptions import ValidationError
from test_plus import TestCase
from maceoutliner.users.validators import validate_usernames_icase


class UserNameValidatorTest(TestCase):
    """
    Tests for custom username validators.
    """

    def setUp(self):
        self.user1 = self.make_user("username_121")
        self.data = {
            "email": "somemonkey@gmail.com",
            "username": "USeRNAME_121",
            "password1": "ohsos67894783278932  sdfhasdfauifh&*(&)",
            "password2": "ohsos67894783278932  sdfhasdfauifh&*(&)",
        }
        self.url_kwargs = {"data": self.data}
        self.view_string = "account_signup"

    def test_icase_username_search(self):
        """
        Try to create another user with the same username in a different case.
        """
        with pytest.raises(ValidationError):
            validate_usernames_icase("USeRNAME_121")

    def test_allauth_incorporates_validator(self):
        """
        Ensure that submitting to the allauth view takes the new validator into account.
        """
        self.post(self.view_string, **self.url_kwargs)
        self.response_200()
        form = self.get_context("form")
        print(form.errors)
        assert len(form.errors) == 1
        assert (
            form.errors["username"][0]
            == "This username is already taken. Please select another."
        )
