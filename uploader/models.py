# uploader/models.py
from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to="uploads/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return f"Document {self.id} - {self.file.name}"
