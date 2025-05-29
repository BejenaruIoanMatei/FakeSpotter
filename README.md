# FakeSpotter
### Deepfake Image Detection Using CNNs

FakeSpotter is a web-based application built with Django that detects fake images with people using deep learning.

The system supports image classification powered by convolutional neural networks (CNNs), integrating models trained with both PyTorch and TensorFlow.

If you are curious about the models you can find the google colab notebook here: [FakeSpotterNotebook](https://colab.research.google.com/drive/1nizvdocMwvu0jHFwLm4kl41wXcCbPnZd?usp=sharing)

> **Note:** The Django implementation is not production-ready yet, but I do plan to optimize it further. For now, it serves as a simple web app to showcase the core feature — detecting fake images of people.

### Features

- Web interface built with Django
- Image Upload and deepfake detection in real time
- Trained and evaluated using both:
  - ResNet18 and InceptionV3 (PyTorch)
  - InceptionV3 (tensorflow, final integrated model)

### Model Training

- Model training and evaluation were done in a jupyter notebook using google colab due to local hardware limitations (my machine is not that great).

> **Note:** This project won’t run locally out-of-the-box, as it uses pretrained models that were downloaded and saved locally (not committed to the repository)

### Demo video

Link to demo: [FakeSpotterDemo](https://drive.google.com/file/d/1U4um_sSfgT2GiO9d0UellwZTQPimJ-aD/view?usp=drive_link)
