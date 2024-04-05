from django.test import TestCase
from django.contrib.auth.models import User
from .models import Goal
from datetime import date

class GoalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # テスト用ユーザーと目標の作成
        test_user = User.objects.create_user(username='testuser', password='12345')
        Goal.objects.create(user=test_user, title='Test Goal', description='Test Description', achievement_percentage=50)

    def test_goal_achievement_percentage(self):
        goal = Goal.objects.get(id=1)
        expected_achievement_percentage = 50
        self.assertEquals(goal.achievement_percentage, expected_achievement_percentage)

class GoalModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # テスト用ユーザーと目標の作成
        test_user = User.objects.create_user(username='testuser', password='12345')
        Goal.objects.create(
            user=test_user, 
            title='Test Goal', 
            description='Test Description', 
            achievement_percentage=50,
            deadline=date.today()  # ここでdeadlineに値を設定
        )