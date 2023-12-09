# tests.py
# from django.test import TestCase, Client
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
# from .models import UploadedFile

# class FileSharingSystemTests(TestCase):

#     def setUp(self):
#         # Create Ops User for testing
#         self.ops_user = User.objects.create_user(username='ops_user', password='ops_password')
#         self.ops_token = Token.objects.create(user=self.ops_user)

#         # Create Client User for testing
#         self.client_user = User.objects.create_user(username='client_user', password='client_password')
#         self.client_token = Token.objects.create(user=self.client_user)

#     def test_ops_user_login(self):
#         # Test Ops User login API
#         response = self.client.post('/ops/login/', {'username': 'ops_user', 'password': 'ops_password'})
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('token', response.json())

#     def test_ops_user_upload(self):
#         # Test Ops User file upload API
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.ops_token.key}')
#         with open('path/to/test_file.pptx', 'rb') as file:
#             response = self.client.post('/ops/upload/', {'file': file})
#         self.assertEqual(response.status_code, 201)  # Assuming 201 for successful upload

#     def test_client_user_signup(self):
#         # Test Client User signup API
#         response = self.client.post('/client/signup/', {'username': 'client_user', 'password': 'client_password'})
#         self.assertEqual(response.status_code, 201)

#     def test_client_user_download(self):
#         # Test Client User file download API
#         # Assume there is an uploaded file with ID 1
#         UploadedFile.objects.create(user=self.client_user, file_type='pptx', download_link='secure_download_link')
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.client_token.key}')
#         response = self.client.get('/client/download/1/')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('download-link', response.json())

#     def test_client_user_list_files(self):
#         # Test Client User list files API
#         UploadedFile.objects.create(user=self.client_user, file_type='pptx', download_link='secure_download_link')
#         self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.client_token.key}')
#         response = self.client.get('/client/list-files/')
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('files', response.json())


# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile, UploadedFile

class FileSharingSystemTests(TestCase):

    def setUp(self):
        # Set up test data
        self.ops_user = User.objects.create_user(username='ops_user', password='ops_password')
        self.client_user = User.objects.create_user(username='client_user', password='client_password')
        self.ops_token = self.get_auth_token('ops_user', 'ops_password')
        self.client_token = self.get_auth_token('client_user', 'client_password')

    def get_auth_token(self, username, password):
        client = APIClient()
        response = client.post('/ops/login/', {'username': username, 'password': password})
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data.get('token', '')


    def test_ops_user_upload(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {self.ops_token}')
        
        # Create a test file
        test_file = open('test_file.pptx', 'rb')
        
        response = client.post('/ops/upload/', {'file': test_file, 'file_type': 'pptx'}, format='multipart')
        test_file.close()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_user_signup_and_download(self):
        # Client user signup
        client = APIClient()
        response = client.post('/client/signup/', {'username': 'client_user', 'password': 'client_password', 'email': 'client@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Client user login
        response = client.post('/client/login/', {'username': 'client_user', 'password': 'client_password'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client_token = response.data.get('token', '')

        # Client user downloads a file (replace '1' with a valid file ID)
        response = client.get('/client/download/1/', HTTP_AUTHORIZATION=f'Token {client_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_user_list_files(self):
        # Client user login
        client = APIClient()
        response = client.post('/client/login/', {'username': 'client_user', 'password': 'client_password'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client_token = response.data.get('token', '')

        # Client user lists all uploaded files
        response = client.get('/client/list-files/', HTTP_AUTHORIZATION=f'Token {client_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

if __name__ == '__main__':
    print("\nRunning Tests...\n")
    unittest.main()
