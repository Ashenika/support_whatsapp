from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse
from twilio.rest import Client
from .models import WhatsAppMessage
from notifications.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

class WhatsAppMessageAdmin(admin.ModelAdmin):
    # Display fields in the admin list view
    list_display = ('sender', 'receiver', 'content', 'timestamp', 'status')
    list_filter = ('status', 'timestamp')  # Add filters for status and date
    search_fields = ('sender', 'receiver', 'content')  # Enable search

    # Add a custom page for sending test messages
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-test-message/', self.admin_site.admin_view(self.send_test_message), name='send_test_message'),
        ]
        return custom_urls + urls

    def send_test_message(self, request):
        if request.method == 'POST':
            # Fetch form data
            to_number = request.POST.get('to_number')
            message_body = request.POST.get('message_body')

            # Send message using Twilio
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
            try:
                message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    body=message_body,
                    to=f'whatsapp:+{to_number}'
                )
                # Save the sent message in the database
                WhatsAppMessage.objects.create(
                    sender='whatsapp:+14155238886',
                    receiver=f'whatsapp:+{to_number}',
                    content=message_body,
                    status='sent'
                )
                return HttpResponse("Message sent successfully!")
            except Exception as e:
                return HttpResponse(f"Failed to send message: {str(e)}")

        # Render a simple form for sending messages
        return render(request, 'admin/send_message.html')

# Register the model and admin customization
admin.site.register(WhatsAppMessage, WhatsAppMessageAdmin)