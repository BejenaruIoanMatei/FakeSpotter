import torch
from torchvision import models, transforms
from PIL import Image
import os
from django.conf import settings
from io import BytesIO

MODEL_PATH = '/Users/user/Documents/GitHub/FakeSpotter/detector/models/inception_fake_spotter_binary.pth'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model_correctly():
    """Load model exactly as it was saved during training"""
    try:
        # Initialize EXACTLY as during training
        model = models.inception_v3(weights=None, aux_logits=True)
        
        # Modify both classifiers to match training setup
        model.fc = torch.nn.Linear(model.fc.in_features, 2)
        model.AuxLogits.fc = torch.nn.Linear(768, 2)
        
        # Load the complete state dict
        state_dict = torch.load(MODEL_PATH, map_location=device, weights_only=True)
        
        # Handle potential naming mismatches
        new_state_dict = {}
        for k, v in state_dict.items():
            name = k.replace('module.', '')  # Remove 'module.' if present
            new_state_dict[name] = v
        
        # Load state dict
        model.load_state_dict(new_state_dict, strict=True)
        model = model.to(device)
        model.eval()
        
        print(f"Model loaded successfully on {device}")
        return model
        
    except Exception as e:
        print(f"Error loading model: {e}")
        raise

# Initialize model once when module is imported
model = load_model_correctly()

# Test model after loading
def test_model():
    """Test model with random tensor to ensure it works"""
    try:
        test_tensor = torch.randn(1, 3, 299, 299).to(device)
        with torch.no_grad():
            outputs = model(test_tensor)
            if isinstance(outputs, tuple):
                outputs = outputs[0]
            print("Test output shape:", outputs.shape)
            print("Softmax:", torch.softmax(outputs, dim=1))
            return True
    except Exception as e:
        print(f"Model test failed: {e}")
        return False

# Run test
if test_model():
    print("Model test passed!")
    print("Main classifier:", model.fc)
    print("Aux classifier:", model.AuxLogits.fc)

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((299, 299)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def classify_image_correctly(img_path):
    """
    Classify an image as Real or Fake
    
    Args:
        img_path: Path to image file
        
    Returns:
        tuple: (prediction, confidence)
    """
    try:
        # Verify file exists
        if not os.path.exists(img_path):
            print(f"Image file not found: {img_path}")
            return "Error", 0.0
            
        # Load and process image
        img = Image.open(img_path).convert("RGB")
        print(f"Image loaded - mode: {img.mode}, size: {img.size}")
        
        # Transform image
        img_tensor = transform(img).unsqueeze(0).to(device)
        print(f"Tensor shape: {img_tensor.shape}")
        print(f"Tensor range: [{img_tensor.min().item():.3f}, {img_tensor.max().item():.3f}]")
        
        # Inference
        with torch.no_grad():
            outputs = model(img_tensor)
            
            # Handle aux outputs (model returns tuple in some cases)
            if isinstance(outputs, tuple):
                outputs = outputs[0]  # Use main classifier output
            
            # Get probabilities
            probs = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probs, 1)
            
            confidence = confidence.item()
            predicted = predicted.item()
            
            # Debug info
            print(f"Raw outputs: {outputs.cpu().numpy()}")
            print(f"Probabilities: {probs.cpu().numpy()}")
            print(f"Predicted class: {predicted}, Confidence: {confidence:.4f}")
            
            # Return result
            result = "Real" if predicted == 0 else "Fake"
            return result, float(confidence)
            
    except Exception as e:
        print(f"Classification error: {e}")
        import traceback
        traceback.print_exc()
        return "Error", 0.0

def classify_image_from_upload(uploaded_file):
    """
    Classify an image from Django uploaded file
    
    Args:
        uploaded_file: Django UploadedFile object
        
    Returns:
        tuple: (prediction, confidence)
    """
    try:
        # Read image from uploaded file
        img = Image.open(uploaded_file).convert("RGB")
        print(f"Uploaded image - mode: {img.mode}, size: {img.size}")
        
        # Transform image
        img_tensor = transform(img).unsqueeze(0).to(device)
        
        # Inference
        with torch.no_grad():
            outputs = model(img_tensor)
            
            if isinstance(outputs, tuple):
                outputs = outputs[0]
            
            probs = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probs, 1)
            
            confidence = confidence.item()
            predicted = predicted.item()
            
            print(f"Prediction: {predicted}, Confidence: {confidence:.4f}")
            
            result = "Real" if predicted == 0 else "Fake"
            return result, float(confidence)
            
    except Exception as e:
        print(f"Classification error: {e}")
        return "Error", 0.0

# Function to get model info (useful for debugging)
def get_model_info():
    """Return model information for debugging"""
    return {
        'device': str(device),
        'model_path': MODEL_PATH,
        'main_classifier': str(model.fc),
        'aux_classifier': str(model.AuxLogits.fc),
        'total_params': sum(p.numel() for p in model.parameters()),
        'trainable_params': sum(p.numel() for p in model.parameters() if p.requires_grad)
    }