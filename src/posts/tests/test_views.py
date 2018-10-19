# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import json
import pytest
from mixer.backend.django import mixer
from .base import PostsBaseTest

pytestmark = pytest.mark.django_db


class PostViewsTests(PostsBaseTest):

    def test_create_fake_data_then_send_get_request_via_user_viewset(self):
        # create 50 users
        
        for cnt in range(50):
            mixer.blend('auth.User', is_active=True)

        url = reverse('user-list')
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
            'username' : 'admin',
            'password' : 'anseotjd',
            'email' : 'admin@naver.com',
            'is_active' : True,
        }
        url = reverse('user-list')
        response = self.client.post(url, data=data, format='json')
        response.content
        assert response.status_code == status.HTTP_201_CREATED

    def test_send_retrive_update_destory_request_via_user_viewset(self):

        # post 를 이용해서 유저 생성
        url = reverse('user-list')
        data = {
            'username' : "HiDaesung",
            'password' : "Hello_Ela",
            'email' : 'mmdsds@naver.com',
            'is_active' : True,
        }
        response = self.client.post(url, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.get(pk=1).username == 'HiDaesung'

        url = reverse('user-detail', args=[1])
        response = self.client.get(url, format='json')
        assert response.status_code == status.HTTP_200_OK

        data = {
            'is_active' : False
        }
        url = reverse('user-detail', args=[1])
        response = self.client.patch(url, data=json.dumps(data), content_type='application/json')
        # import ipdb; ipdb.set_trace()
        assert response.status_code == status.HTTP_200_OK
