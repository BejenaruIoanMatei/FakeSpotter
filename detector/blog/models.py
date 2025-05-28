from django.db import models
from django.contrib.auth.models import User

class ImageClassification(models.Model):
    image = models.ImageField(upload_to='uploads/')
    predicted_label = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)  # instead of null=True, blank=True
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.predicted_label} ({self.confidence:.2f})"