from application import create_app as create_app_base
from mongoengine.connection import _get_db
import unittest
from flask import session

from user.models import User


class UserTest(unittest.TestCase):
    '''
    This class inherites unittest.testCase Class
    '''
    def create_app(self):
        '''
        Method for configuring the test
        :return: An Application
        '''
        return create_app_base(
            # Database settings
            MONGODB_SETTINGS={'db': 'user',
                              'host': '192.168.1.2',
                              'port': 27017
                              },
            # it tells flask, we are doing a test
            TESTING=True,
            # cookies and secret_key requirement by
            # WTForms will be disabled
            WTF_CSRF_ENABLED=False,
            # Setting SECRET_KEY for testing the login
            SECRET_KEY='#$#CR$RC$TY^UTR&rgvrt'
        )

    def setUp(self):
        '''
        Setting Up the application
        :return: None
        '''
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()

    def tearDown(self):
        '''
        destroying the database
        :return: None
        '''
        self.db = _get_db()
        # the Following line causes error
        #self.db.client.drop_database()

    def user_dict(self):
        return dict(
            first_name='Julia',
            last_name='Kavalenka',
            username='julia',
            email='julia@ka.com',
            password='test123',
            confirm='test123'
        )

    def test_register_user(self):
        # basic registration
        self.app.post('/register', data=self.user_dict(), follow_redirects=True)
        assert User.objects.filter(username='julia').count() == 1

    def test_login_user(self):
        # Create User
        self.app.post('/register', data=self.user_dict())
        # Logging in
        rv = self.app.post('/login', data=dict(
            username=self.user_dict()['username'],
            password=self.user_dict()['password']
        ))
        # Chcek , if the Session is Set
        with self.app as c:
            rv = c.get('/')
            assert session.get('username') == self.user_dict()['username']