import pytest
from django.core.exceptions import ValidationError
from test_plus import TestCase
from maceoutliner.users.validators import validate_usernames_icase


class UserNameValidatorTest(TestCase):
    '''
    Tests for custom username validators.
    '''

    def setUp(self):
        self.user1 = self.make_user('user1')
        self.data = {
            'email': 'somemonkey@gmail.com',
            'username': 'U1',
            'password1': 'ohsos67894783278932  sdfhasdfauifh&*(&)'
        }
        self.url_kwargs = {
            'data': self.data,
        }
        self.view_string = 'account_signup'

    def test_icase_username_search(self):
        '''
        Try to create another user with the same username in a different case.
        '''
        with pytest.raises(ValidationError):
            validate_usernames_icase('USeR1')
