from test_plus import TestCase
from maceoutliner.users.models import User
from maceoutliner.users.adapters import SocialAccountAdapter


class TestCustomSignup(TestCase):
    '''
    Tests for our custom allauth overrides in the signup form.
    '''

    def setUp(self):
        self.view_string = 'account_signup'
        self.data = {
            'username': 'daniel42',
            'email': 'admin@andrlik.org',
            'display_name': 'I am a monkey!',
            'password1': 'jfkdhsfjkdhudh&&(&*^*&%%^*)',
            'password2': 'jfkdhsfjkdhudh&&(&*^*&%%^*)',
        }
        self.data2 = {
            'username': 'daniel42',
            'email': 'admin@andrlik.org',
            'password1': 'jfkdhsfjkdhudh&&(&*^*&%%^*)',
            'password2': 'jfkdhsfjkdhudh&&(&*^*&%%^*)',
        }
        self.url_kwargs = {
            'data': self.data
        }
        self.url_kwargs2 = {
            'data': self.data2
        }

    def test_custom_signup(self):
        '''
        Ensure that the additional display_name field gets populated to user.
        '''
        before_signup = User.objects.all().count()
        self.post(self.view_string, **self.url_kwargs)
        self.response_302()  # No errors
        assert User.objects.all().count() - before_signup == 1
        user = User.objects.get(username='daniel42')
        assert user.display_name == 'I am a monkey!'

    def test_custom_signup_without_value(self):
        '''
        Ensure a signup does not fail with display_name is not provided.
        '''
        before_signup = User.objects.all().count()
        self.post(self.view_string, **self.url_kwargs2)
        self.response_302()
        assert User.objects.all().count() - before_signup == 1
        user = User.objects.get(username='daniel42')
        assert user.display_name is None
