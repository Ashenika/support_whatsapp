from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import WhatsAppMessage
from unittest.mock import patch

# Create your tests here.
class ViewsTestCase(TestCase):
    def setUp(self):
        """
        Set up test environment:
        - Create a test user
        - Set up the test client
        """
        self.client = Client()
        self.user = User.objects.create_user(username="admin", password="admin")
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.send_message_url = reverse('send_message')
        self.list_messages_url = reverse('list_messages')
        self.view_message_url = lambda message_id: reverse('view_message', args=[message_id])
        self.webhook_url = reverse('webhook')

    def test_user_login_success(self):
        """
        Test that a user can successfully log in.
        """
        response = self.client.post(self.login_url, {"username": "admin", "password": "admin"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.list_messages_url)

    def test_user_login_failure(self):
        """
        Test that an invalid login attempt fails.
        """
        response = self.client.post(self.login_url, {"username": "testuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid credentials")
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_user_logout(self):
        """
        Test that a logged-in user can successfully log out.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # Assert the user is logged out
        response = self.client.get(self.list_messages_url)
        self.assertEqual(response.status_code, 302)

    @patch('twilio.rest.api.v2010.account.message.MessageList.create')
    def test_send_message_success(self, mock_twilio_create):
        """
        Test sending a WhatsApp message successfully.
        """
        self.client.login(username="admin", password="admin")
        mock_twilio_create.return_value.sid = "12345"

        response = self.client.post(self.send_message_url, {
            "user_number": "94123456789",
            "message_body": "Hello, this is a test message!"
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Message sent successfully!")
        self.assertTrue(WhatsAppMessage.objects.filter(receiver="whatsapp:+94123456789").exists())

        # Assert the mock create method was called with correct parameters
        mock_twilio_create.assert_called_once_with(
            from_='whatsapp:+14155238886',
            body="Hello, this is a test message!",
            to="whatsapp:+94123456789"
        )

    def test_send_message_missing_fields(self):
        """
        Test sending a message with missing fields.
        """
        self.client.login(username="admin", password="admin")
        response = self.client.post(self.send_message_url, {
            "user_number": "",
            "message_body": ""
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "All fields are required")

    def test_list_messages(self):
        """
        Test listing messages.
        """
        self.client.login(username="admin", password="admin")
        WhatsAppMessage.objects.create(
            sender="whatsapp:+14155238886",
            receiver="whatsapp:+94123456789",
            content="Test message",
            status="sent"
        )

        response = self.client.get(self.list_messages_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test message")

    def test_view_message(self):
        """
        Test viewing a specific message.
        """
        self.client.login(username="admin", password="admin")
        message = WhatsAppMessage.objects.create(
            sender="whatsapp:+14155238886",
            receiver="whatsapp:+94123456789",
            content="Test message",
            status="sent"
        )

        response = self.client.get(self.view_message_url(message.id))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test message")

    def test_webhook_success(self):
        """
        Test the webhook successfully processes an incoming message.
        """
        payload = {
            "From": "whatsapp:+94123456789",
            "To": "whatsapp:+14155238886",
            "Body": "Incoming test message"
        }

        response = self.client.post(self.webhook_url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "success")
        self.assertTrue(WhatsAppMessage.objects.filter(sender="whatsapp:+94123456789").exists())

    def test_webhook_missing_fields(self):
        """
        Test the webhook with missing fields.
        """
        payload = {
            "From": "",
            "To": "",
            "Body": ""
        }

        response = self.client.post(self.webhook_url, payload)
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Incomplete data", status_code=400)