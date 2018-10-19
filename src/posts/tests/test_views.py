# -*- coding: utf-8 -*-
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils import timezone
from rest_framework import status
from mixer.backend.django import mixer
from oauth2_provider.models import get_application_model, AccessToken

from .base import PostsBaseTest

import json
import pytest

pytestmark = pytest.mark.django_db

Application = get_application_model()


class PostViewsTests(PostsBaseTest):

    def test_create_fake_data_then_send_get_request_via_user_viewset(self):

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
            expires=timezone.now() + timedelta(minutes=5),
            token=f'{random}---{admin_user.username}',
            application=app
        )

        # create 50 users

        for cnt in range(50):
            mixer.blend('auth.User', is_active=True)

        url = reverse('user-list')

        # 이 부분이 포인트, 토큰을 넣음
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {admin_token.token}'
        )
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_send_get_request_via_user_viewset(self):
        # list GET : POST
        # retrive / patch / des /  GET:PUT:DELETE

        url = reverse('user-list')
        response = self.client.get(url, format='json')

        assert response.status_code == status.HTTP_200_OK

    def test_send_post_request_via_user_viewset(self):
        # list GET : POST
        # retrive / patch / des /  GET:PUT:DELETE
        data = {
            'username': 'admin',
            'password': 'anseotjd',
            'email': 'admin@naver.com',
            'is_active': True,
        }
        url = reverse('user-list')
        response = self.client.post(url, data=data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED

    def test_send_retrive_update_destory_request_via_user_viewset(self):

        # post 를 이용해서 유저 생성
        url = reverse('user-list')
        data = {
            'username': "HiDaesung",
            'password': "Hello_Ela",
            'email': 'mmdsds@naver.com',
            'is_active': True,
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.get(pk=1).username == 'HiDaesung'

        url = reverse('user-detail', args=[1])
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK

        data = {
            'is_active': False
        }
        url = reverse('user-detail', args=[1])
        response = self.client.patch(url, data=json.dumps(
            data), content_type='application/json')
        # import ipdb; ipdb.set_trace()
        assert response.status_code == status.HTTP_200_OK
