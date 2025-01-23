from django.db import models

# Create your models here.
class WhatsAppMessage(models.Model):
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('read', 'Read'),
            ('failed', 'Failed'),
        ],
        default='sent'
    )

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.status}"
