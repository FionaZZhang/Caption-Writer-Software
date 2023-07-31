from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import torch
from torchvision import models, transforms
from PIL import Image
import requests
from io import BytesIO
import openai
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['UPLOAD_FOLDER'] = './uploads'
openai.api_key = ''


# Load the pre-trained MobileNetV2 model
model = models.mobilenet_v2(pretrained=False)
model.load_state_dict(torch.load("mobilenet_v2.pth")) #https://download.pytorch.org/models/mobilenet_v2-b0353104.pth
model.eval()

# Load the class labels used by the pre-trained model
LABELS_URL = 'https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json'
labels = requests.get(LABELS_URL).json()

transform = transforms.Compose([  # [1]
    transforms.Resize(256),  # [2]
    transforms.CenterCrop(224),  # [3]
    transforms.ToTensor(),  # [4]
    transforms.Normalize(  # [5]
        mean=[0.485, 0.456, 0.406],  # [6]
        std=[0.229, 0.224, 0.225]  # [7]
    )])


def analyze_image(image_path):
    image = Image.open(image_path)
    image = image.resize((224, 224))
    image = transform(image)
    image = image.unsqueeze(0)
    with torch.no_grad():
        preds = model(image)
        _, indices = torch.topk(preds, 3)
        probs = torch.nn.functional.softmax(preds, dim=1)[0] * 100
        top_classes = [labels[idx] for idx in indices[0]]

    image = Image.open(image_path)
    image = image.resize((25, 25))
    colors = image.getcolors(image.size[0] * image.size[1])
    most_frequent_color = sorted(colors, key=lambda x: x[0], reverse=True)[0][1]
    dominant_color = ' '.join(map(str, most_frequent_color))

    tags = top_classes + [dominant_color]
    print(tags)
    return tags

def generate_caption(image_tags, user_input):
    prompt = "Here are the objects and color in the picture: " + ", ".join(image_tags) + " " + "Here is the user's requirement" + user_input
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=100,
        messages=[
            {"role": "system", "content": "You are generating a caption (for making a wechat post) for a picture. "},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

@app.route('/')
def index():
    return render_template('blogApp.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_tags = analyze_image(filepath)
            user_input = request.form.get('user_input', '')
            caption = generate_caption(image_tags, user_input)
            return jsonify({"caption": caption}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)