from django.db import models

# Create your models here.
class WhatsAppMessage(models.Model):
    """
        Represents a WhatsApp message sent or received via the application.

        Attributes:
            sender (str): The WhatsApp number of the message sender.
            receiver (str): The WhatsApp number of the message receiver.
            content (str): The content of the message.
            timestamp (datetime): The date and time when the message was created.
            status (str): The status of the message (e.g., sent, delivered, read, failed).
    """
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ]
    sender = models.CharField(max_length=255, help_text="The sender's WhatsApp number (e.g., whatsapp:+1234567890)")
    receiver = models.CharField(max_length=255, help_text="The receiver's WhatsApp number (e.g., whatsapp:+0987654321)")
    content = models.TextField(help_text="The content of the WhatsApp message")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="The date and time the message was created")
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='sent',
        help_text="The current status of the message"
    )

    class Meta:
        verbose_name = "WhatsApp Message"
        verbose_name_plural = "WhatsApp Messages"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.status}"
