from twilio.rest import Client
from notifications.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import WhatsAppMessage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging

logging.basicConfig(level=logging.DEBUG)

# Login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('send_message')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# Logout view
def user_logout(request):
    logout(request)
    return redirect('login')


# Send message view
@login_required
def send_message(request):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    if request.method == 'POST':
        user_whatsapp_number = request.POST['user_number']
        message_body = request.POST['message_body']

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message_body,
            to=f'whatsapp:+{user_whatsapp_number}'
        )

        # Save message to the database
        WhatsAppMessage.objects.create(
            sender='whatsapp:+14155238886',
            receiver=f'whatsapp:+{user_whatsapp_number}',
            content=message_body,
            status='sent'
        )

        print(user_whatsapp_number)
        print(message.sid)
        return render(request, 'send_message.html', {'success': 'Message sent successfully!'})

    return render(request, 'send_message.html')

# List messages view
@login_required
def list_messages(request):
    messages = WhatsAppMessage.objects.order_by('-timestamp')
    return render(request, 'list_messages.html', {'messages': messages})

# View a received message
@login_required
def view_message(request, message_id):
    message = get_object_or_404(WhatsAppMessage, id=message_id)
    return render(request, 'view_message.html', {'message': message})

@csrf_exempt
def webhook(request):
    if request.method == 'POST':
        # Log headers and body for debugging
        print("Webhook triggered!")
        print(f"Headers: {request.headers}")
        print(f"Raw Body: {request.body}")

        # Extract data from POST payload
        sender = request.POST.get('From', '')
        receiver = request.POST.get('To', '')
        content = request.POST.get('Body', '')

        print(f"Extracted Data - Sender: {sender}, Receiver: {receiver}, Content: {content}")

        if sender and receiver and content:
            try:
                # Save the message to the database
                WhatsAppMessage.objects.create(
                    sender=sender,
                    receiver=receiver,
                    content=content,
                    status='received'
                )
                print("Message saved successfully!")
                return JsonResponse({"status": "success"})
            except Exception as e:
                print(f"Error saving message: {e}")
                return JsonResponse({"error": "Database save failed"}, status=500)
        else:
            print("Incomplete data received!")
            return JsonResponse({"error": "Incomplete data"}, status=400)
    else:
        print("Invalid request method!")
        return JsonResponse({"error": "Invalid request method"}, status=400)
