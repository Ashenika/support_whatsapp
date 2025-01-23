from notifications.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_SANDBOX_NUMBER
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import WhatsAppMessage
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)

def user_login(request):
    """
        Handles user login.

        - If the request method is POST, authenticate the user using the provided username and password.
        - If the authentication succeeds, logs the user in and redirects to the message list page.
        - If authentication fails, renders the login page with an error message.

        Parameters:
            request (HttpRequest): The HTTP request object containing metadata about the request.

        Returns:
            HttpResponse: The rendered login page or a redirect to the message list.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_messages')
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def user_logout(request):
    """
        Handles user logout.

        Parameters:
            request (HttpRequest): The HTTP request object containing metadata about the request.

        Returns:
            redirection to login page.
    """
    logout(request)
    return redirect('login')


@login_required
def send_message(request):
    """
        Handles send whatsapp message.

        Parameters:
            request (HttpRequest): The HTTP request object containing metadata about the request.

        Returns:
            render with request data to html page.
    """
    if request.method == 'POST':
        user_whatsapp_number = request.POST['user_number']
        message_body = request.POST['message_body']

        if not user_whatsapp_number or not message_body:
            logger.error("Missing required fields: user_number or message_body")
            return render(request, 'send_message.html', {'error': 'All fields are required'})

        try:
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                from_=f'whatsapp:{TWILIO_SANDBOX_NUMBER}',
                body=message_body,
                to=f'whatsapp:+{user_whatsapp_number}'
            )

            # Save message to the database
            WhatsAppMessage.objects.create(
                sender=f'whatsapp:{TWILIO_SANDBOX_NUMBER}',
                receiver=f'whatsapp:+{user_whatsapp_number}',
                content=message_body,
                status='sent'
            )
            logger.info(f"Message sent to {user_whatsapp_number}. Twilio SID: {message.sid}")
            return render(request, 'send_message.html', {'success': 'Message sent successfully!'})

        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return render(request, 'send_message.html', {'error': 'Failed to send message'})

    return render(request, 'send_message.html')

@login_required
def list_messages(request):
    """
        View list of messages.

        Parameters:
            request (HttpRequest): The HTTP request object containing metadata about the request.

        Returns:
            render with request and messages data to list html page.
    """
    messages = WhatsAppMessage.objects.order_by('-timestamp')
    return render(request, 'list_messages.html', {'messages': messages})

@login_required
def view_message(request, message_id):
    """
        View single message.

        Parameters:
            request (HttpRequest): The HTTP request object containing metadata about the request.
            message_id: ID of the message.

        Returns:
            render with request and message data to view message html page.
    """
    message = get_object_or_404(WhatsAppMessage, id=message_id)
    return render(request, 'view_message.html', {'message': message})

@csrf_exempt
def webhook(request):
    """
        Handles incoming WhatsApp messages via Twilio Webhook.

        - This view processes POST requests sent by Twilio's webhook.
        - Extracts the sender, receiver, and message content from the request.
        - Saves the message to the database with a "received" status.

        Parameters:
            request (HttpRequest): The HTTP request object containing the Twilio POST payload.

        Returns:
            JsonResponse: Success or error message depending on the outcome.
    """
    if request.method == 'POST':
        logger.info("Webhook triggered!")

        # Extract data from POST payload
        sender = request.POST.get('From', '')
        receiver = request.POST.get('To', '')
        content = request.POST.get('Body', '')

        if sender and receiver and content:
            try:
                # Save the message to the database
                WhatsAppMessage.objects.create(
                    sender=sender,
                    receiver=receiver,
                    content=content,
                    status='received'
                )
                logger.info(f"Message saved successfully: Sender={sender}, Receiver={receiver}")
                return JsonResponse({"status": "success"})
            except Exception as e:
                logger.error(f"Error saving webhook message: {e}")
                return JsonResponse({"error": "Database save failed"}, status=500)
        else:
            logger.warning("Incomplete data received!")
            return JsonResponse({"error": "Incomplete data"}, status=400)
    else:
        logger.warning("Invalid request method for webhook")
        return JsonResponse({"error": "Invalid request method"}, status=400)
