import mimetypes

from django.contrib.auth import get_user_model
from django.db import models, transaction


# Create your models here.
class ChatFile(models.Model):
    file = models.FileField(upload_to="chat/files/")
    mimetype = models.CharField(null=True, blank=True, max_length=100)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.mimetype:
            self.mimetype = self.get_mimetype()

        return super().save(*args, **kwargs)

    def get_mimetype(self):
        return mimetypes.guess_type(self.file.name)[0]


class ChatRoom(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.user + "-" + str(self.id)


class ChatMessage(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    files = models.ManyToManyField("ChatFile", blank=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    index = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.room} - {self.message} {self.date}"

    class Meta:
        ordering = ("date",)
        unique_together = ("room", "index")

    def save(self, *args, **kwargs):
        with transaction.atomic():
            # Retrieve the current maximum index value within the room
            max_index = ChatMessage.objects.filter(room=self.room).aggregate(models.Max("index"))["index__max"] or 0

            # Increment the index by 1 using F() expression and save the object
            self.index = max_index + 1
            super().save(*args, **kwargs)

    def last_message(self):
        try:
            return ChatMessage.objects.filter(room=self.room, index__lte=self.index - 1, deleted=False).last()
        except Exception:
            return

    def next_messages(self):
        messages = ChatMessage.objects.filter(room=self.room, index__gt=self.index, deleted=False)

        end = messages.exclude(user=self.user).filter(index__gt=self.index)
        if end.exists():
            messages = messages.filter(index__lt=end[0].index)
        return messages
