from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
   id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)

   phone_number = models.CharField(max_length=20, null=True, blank=True)

   ROLE_CHOICES = (
      ('guest', 'Guest'),
      ('host', 'Host'),
      ('admin', 'Admin'),
   )

role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")

created_at = models.DateTimeField(auto_now_add=True)

 # Email must be unique (Django User already includes email)
email = models.EmailField(unique=True)

# username is required by AbstractUser unless you disable it
 # We keep it for simplicity.

def __str__(self):
    return f"{self.username} ({self.email})"


# -----------------------------------------
# Conversation Model
# -----------------------------------------
    class Conversation(models.Model):
        """
        A chat conversation with 2 or more participants.
        """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    participants = models.ManyToManyField(User, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# -----------------------------------------
# Message Model
# -----------------------------------------
class Message(models.Model):
    """
    Messages inside a conversation.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )

    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"