# views.py - Versiunea simplificată

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from .models import ImageClassification
from .forms import ImageUploadForm
from .fake_spotter_utils import classify_image

class ClassifierView(CreateView):
    model = ImageClassification
    form_class = ImageUploadForm
    template_name = 'blog/classifier.html'
    success_url = reverse_lazy('blog-classifier')

    def form_valid(self, form):
        # Setează un utilizator dummy sau primul utilizator din baza de date
        try:
            dummy_user = User.objects.first()
            if not dummy_user:
                # Creează un utilizator dummy dacă nu există niciunul
                dummy_user = User.objects.create_user(
                    username='anonymous',
                    email='anonymous@example.com'
                )
            form.instance.user = dummy_user
        except:
            pass
            
        # Salvează imaginea în model
        response = super().form_valid(form)
        
        # Clasifică imaginea
        img_path = self.object.image.path
        label, confidence = classify_image(img_path)
        
        # Salvează rezultatul
        self.object.predicted_label = label
        self.object.confidence = confidence
        self.object.save(update_fields=['predicted_label', 'confidence'])
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['classifier'] = ImageClassification.objects.last()
        return context
