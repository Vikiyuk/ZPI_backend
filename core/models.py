from django.db import models

class Photo(models.Model):
    image = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
