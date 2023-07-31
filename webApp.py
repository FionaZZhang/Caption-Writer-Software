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
from webcolors import CSS3_NAMES_TO_HEX, hex_to_rgb

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['UPLOAD_FOLDER'] = './uploads'
openai.api_key = ''

# Load the pre-trained MobileNetV2 model
model = models.mobilenet_v2(pretrained=False)
model.load_state_dict(torch.load("mobilenet_v2.pth"))
model.eval()

# Load the class labels used by the pre-trained model
LABELS_URL = 'https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json'
labels = requests.get(LABELS_URL).json()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])

def closest_color(requested_color):
    min_colors = {}
    # calculate euclidean distance between the requested RGB value and all CSS3 color names,
    # storing the difference and color name as key-value pairs in the dictionary
    for key, name in CSS3_NAMES_TO_HEX.items():
        r_c, g_c, b_c = hex_to_rgb(name)
        rd = (r_c - requested_color[0]) ** 2
        gd = (g_c - requested_color[1]) ** 2
        bd = (b_c - requested_color[2]) ** 2
        min_colors[(rd + gd + bd)] = key
    return min_colors[min(min_colors.keys())]  # get the color name with the smallest Euclidean distance

def get_color_name(rgb_tuple):
    closest_name = closest_color(rgb_tuple)
    return closest_name

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
    dominant_color = get_color_name(most_frequent_color)

    tags = top_classes + [dominant_color]
    return tags

def analyze_images(image_paths):
    all_tags = []
    for image_path in image_paths:
        image_tags = analyze_image(image_path)
        all_tags += image_tags
    print(all_tags)
    return all_tags

def generate_caption(image_tags, user_input):
    prompt = "Here are the objects and color in the picture: " + ", ".join(image_tags) + ". " + "Here is the user's requirement: " + user_input
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
        if 'files' not in request.files:
            return jsonify({"error": "No file part"}), 400
        files = request.files.getlist('files')
        if len(files) == 0:
            return jsonify({"error": "No selected file"}), 400
        if len(files) > 9:
            return jsonify({"error": "Too many files. Maximum allowed is 9."}), 400
        filepaths = []
        for file in files:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            filepaths.append(filepath)
        image_tags = analyze_images(filepaths)
        user_input = request.form.get('user_input', '')
        caption = generate_caption(image_tags, user_input)
        return jsonify({"caption": caption}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
