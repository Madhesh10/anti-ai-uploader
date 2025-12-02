from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Chunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    chunk_id = models.IntegerField()
    page = models.IntegerField(null=True)
    text = models.TextField()
    faiss_index = models.IntegerField(null=True)
