# -*- coding: utf-8 -*-

from django.test import TestCase

class TestPostsTest(TestCase):

    def test_smoke_test(self): # 무조건 assert를 해봐야 한다. spot을 터뜨리는 것
        assert 1 is not 1, "당연히 같아야 해요"
