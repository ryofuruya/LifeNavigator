from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Memo

class MemoSearchTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')
        Memo.objects.create(user=cls.user, title="Test Memo 1", content="This is a test memo.")
        Memo.objects.create(user=cls.user, title="Another Test Memo", content="This is another test memo specifically.")

    def test_memo_search_no_keyword(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('memos:memo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['memos']), 2)

    def test_memo_search_with_keyword(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('memos:memo_list'), {'keyword': 'specifically'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['memos']), 1)
