from django.db import models
from django.contrib.auth.models import User
from PIL import Image, UnidentifiedImageError

class ImageClassification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='classified_images')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    predicted_label = models.CharField(max_length=100, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.image.path)
            
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            if img.height > 400 or img.width > 400:
                output_size = (400,400)
                img.thumbnail(output_size)
                img.save(self.image.path)
                
        except UnidentifiedImageError:
            print(f"Could not identify image at {self.image.path}")

    def __str__(self):
        return f"{self.user.username} - {self.predicted_label or 'Unclassified'}"