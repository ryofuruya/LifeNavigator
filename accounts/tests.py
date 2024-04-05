from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile

class UserTestCase(TestCase):

    def setUp(self):
        # テスト用の画像ファイルを作成
        test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open('path/to/your/test_image.jpg', 'rb').read(),
            content_type='image/jpeg'
        )
        
        # テストユーザーを作成
        test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        
        # UserProfileインスタンスを作成し、テスト用の画像ファイルをimageフィールドに設定
        UserProfile.objects.create(user=test_user, image=test_image)

    def test_user_creation(self):
        # テストユーザーが正しく作成されたことを確認
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)
        # UserProfileが正しく作成されたことを確認
        user_profile_count = UserProfile.objects.count()
        self.assertEqual(user_profile_count, 1)
