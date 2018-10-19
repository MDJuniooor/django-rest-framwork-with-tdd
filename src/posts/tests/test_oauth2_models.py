from datetime import timedelta
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.crypto import get_random_string
from django.utils import timezone
from mixer.backend.django import mixer
from oauth2_provider.models import get_application_model, AccessToken

import pytest
pytestmark = pytest.mark.django_db

# 모델이 없어도 셋팅된 모델을 가져온다.
Application = get_application_model()

class TestOauth2Model(TestCase):

    def test_create_oauth2_app(self):
        admin_user = mixer.blend('auth.User', is_staff=True, is_superuser=True)
        app = Application.objects.create(
            name="SuperAPI OAUTH2 App",
            user=admin_user,
            client_type = Application.CLIENT_PUBLIC,
            authorization_grant_type = Application.GRANT_PASSWORD,
        )
        assert Application.objects.count() == 1, "Should be equal"

    def test_create_oauth2_token(self):
        admin_user = mixer.blend('auth.User', is_staff=True, is_superuser=True)
        app = Application.objects.create(
            name="SuperAPI OAUTH2 App",
            user=admin_user,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        assert Application.objects.count() == 1, "Should be equal"

        random = get_random_string(length=16)
       
        admin_token = AccessToken.objects.create(
            user=admin_user,
            scope='read write',
            expires= timezone.now() + timedelta(minutes=5),
            token=f'{random}---{admin_user.username}',
            application=app
        )
        assert admin_token is not None, "널값은 ㄴㄴ"