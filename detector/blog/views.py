from django.shortcuts import render
from django.views.generic import View
from .models import ImageClassification
from .fake_spotter_utils import classify_image_correctly

class ClassifierView(View):
    template_name = 'blog/classifier.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        if 'image' not in request.FILES:
            return render(request, self.template_name, {'error': 'No image uploaded'})

        image_file = request.FILES['image']
        classification = ImageClassification(image=image_file)
        classification.save()

        label, confidence = classify_image_correctly(classification.image.path)
        classification.predicted_label = label
        classification.confidence = confidence
        classification.save()

        return render(request, self.template_name, {
            'result': classification,
            'image_url': classification.image.url
        })