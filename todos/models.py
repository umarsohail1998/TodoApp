from django.db import models

# Create your models here.
class Todo(models.Model):
    content = models.TextField()
    username = models.TextField(default=None)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.content