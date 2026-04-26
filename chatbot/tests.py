from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest.mock import patch
import json

User = get_user_model()

class ChatbotViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = Client()
        self.client.login(username='testuser', password='password')
        self.url = reverse('chatbot:chatbot_send')

    @patch('chatbot.views.get_department_recommendation')
    def test_chatbot_view_json_payload(self, mock_recommend):
        mock_recommend.return_value = {
            'found': True,
            'message': 'Based on your symptoms, we recommend the Cardiology department.',
            'department': 'Cardiology',
        }
        
        response = self.client.post(
            self.url,
            data=json.dumps({'message': 'chest pain'}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['found'])
        self.assertEqual(data['message'], 'Based on your symptoms, we recommend the Cardiology department.')
        mock_recommend.assert_called_once()
        # Verify the message passed to the mock
        self.assertEqual(mock_recommend.call_args[0][0], 'chest pain')

    def test_chatbot_view_empty_message(self):
        response = self.client.post(
            self.url,
            data=json.dumps({'message': ''}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['found'])
        self.assertEqual(data['message'], 'Please describe your symptoms so I can help you.')

    @patch('chatbot.views.get_department_recommendation')
    def test_chatbot_view_form_payload(self, mock_recommend):
        # Verify it still works with traditional form data
        mock_recommend.return_value = {
            'found': True,
            'message': 'Recommendation for headache',
            'department': 'Neurology',
        }
        
        response = self.client.post(
            self.url,
            data={'message': 'headache'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['found'])
        self.assertEqual(data['message'], 'Recommendation for headache')
