from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import torch
from torchvision import models, transforms
from PIL import Image
import requests
import openai
import os
from werkzeug.utils import secure_filename
from webcolors import CSS3_NAMES_TO_HEX, hex_to_rgb
import random

app = Flask(__name__)
CORS(app, supports_credentials=True)
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
app.config['UPLOAD_FOLDER'] = './uploads'
openai.api_key = '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'
current_caption = ''
current_language = ''
current_platform = ''
current_tags = ''
current_requirements = ''
user_caption = ''
current_tags_top = ''

# Define the template prompts
prompts_english = [
    "1. A quote from a book or movie or celebrity, cite where it comes from.",
    "2. Using only emojis.",
    "3. An interesting word or sentence in an European language except English and Chinese, include a translation.",
    "4. A caption that you think is appropriate"
]

prompts_chinese = [
    "1. 书或电影或名人语录中的一句话",
    "2. 只用表情（emojis）",
    "3. 欧洲小语种的一个有意思的词或者一句话，给出中文翻译",
    "4. 一个你觉得合适的文案"
]

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
    global current_tags_top
    image = Image.open(image_path)

    # Check if image is not jpg
    if image_path.split('.')[-1].lower() != 'jpg':
        # Change the path to jpg
        image_path = os.path.splitext(image_path)[0] + '.jpg'
        # Convert image to jpg and save it
        image.convert('RGB').save(image_path)
        # Open the new jpg image
        image = Image.open(image_path)

    image = image.resize((224, 224))
    image = transform(image)
    image = image.unsqueeze(0)
    with torch.no_grad():
        preds = model(image)
        _, indices = torch.topk(preds, 5)
        probs = torch.nn.functional.softmax(preds, dim=1)[0] * 100
        top_classes = [labels[idx] for idx in indices[0]]

        _, indices = torch.topk(preds, 2)
        top_one_classes = [labels[idx] for idx in indices[0]]

    image = Image.open(image_path)
    image = image.resize((25, 25))
    colors = image.getcolors(image.size[0] * image.size[1])
    most_frequent_color = sorted(colors, key=lambda x: x[0], reverse=True)[0][1]
    dominant_color = get_color_name(most_frequent_color)

    tags = top_classes + [dominant_color]
    current_tags_top = top_one_classes

    return tags

def analyze_images(image_paths):
    all_tags = []
    for image_path in image_paths:
        image_tags = analyze_image(image_path)
        all_tags += image_tags
    return all_tags

def generate_caption(image_tags, requirements, caption, language, platform):
    # Prepare the prompt based on the language
    if language == "English":
        final_prompt = (
            "You are a social media influencer. You need to come up with some captions for making a social media post (do not include hashtags #). "
            f"Caption is for the platform {platform}. "
            f"Other requirements from the user: {requirements if requirements else 'None'}. "
            f"Caption provided by the user: {caption if caption else 'None'}. "
            "Here are the 4 captions that you need to generate (response in format no. Your Response): "
            f"{'; '.join(prompts_english)}. "
            "Here are the words describing the pictures, get the vibe not the actual words: "
            f"{', '.join(image_tags) if image_tags else 'None'}."
        )
    else:
        final_prompt = (
            "你是一位网红。你要给一些即将发送的图片想文案。不要在文案中加话题标签。"
            f"你要发送帖子的平台是 {platform}。"
            f"其他的要求: {requirements if requirements else '无'}。"
            f"用户提供的文案: {caption if caption else '无'}。"
            "请给出四个文案（回答请用排版：数字. 文案）: "
            f"{'; '.join(prompts_chinese)}。 "
            f"这里是描述图片的一些词： {', '.join(image_tags) if image_tags else '无'}。用中文回答。"
        )

    print(final_prompt)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.9,
        max_tokens=200,
        messages=[
            {"role": "system", "content": final_prompt}
        ]
    )

    return response.choices[0].message["content"]


def generate_new_caption(index):
    print(current_language)
    if current_language == 'Chinese':
        prompt = (
            "你是一位网红。你要给一些即将发送的图片想文案。不要在文案中加话题标签。"
            f"你要发送帖子的平台是 {current_platform}。"
            f"其他的要求: {current_requirements if current_requirements else '无'}。"
            f"用户提供的文案: {user_caption if user_caption else '无'}。"
            f"请根据第{index}条要求给出一条文案（只要一条，回答模版请用 ’{index}. 你的回答‘）: "
            f"{'; '.join(prompts_chinese)}。 "
            f"这里是描述图片的一些词： {', '.join(current_tags) if current_tags else '无'}。用中文回答。"
        )
    else:
        prompt = (
            "You are a social media influencer. You need to come up with some captions for making a social media post (do not include hashtags #). "
            f"Caption is for the platform {current_platform}. "
            f"Other requirements from the user: {current_requirements if current_requirements else 'None'}. "
            f"Caption provided by the user: {user_caption if user_caption else 'None'}. "
            f"Please generate one single caption according to requirement number {index}: "
            f"{'; '.join(prompts_english)}. "
            "Here are the words describing the pictures, get the vibe not the actual words: "
            f"{', '.join(current_tags) if current_tags else 'None'}."
        )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.9,
        max_tokens=200,
        messages=[
            {"role": "system", "content": prompt}
        ]
    )
    print(prompt)
    print(response.choices[0].message["content"])
    return response.choices[0].message["content"]

@app.route('/')
def index():
    return render_template('blogApp.html')


@app.route('/generate', methods=['POST'])
def generate():
    global current_caption
    global current_language
    global current_platform
    global current_tags
    global current_requirements
    global user_caption
    try:
        files = request.files.getlist('files')
        if files:
            filepaths = []
            for file in files:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                filepaths.append(filepath)
            image_tags = analyze_images(filepaths)
        else:
            image_tags = []

        requirements = request.form.get('requirements', '')
        caption = request.form.get('caption', '')
        language = request.form.get('language', 'English')
        platform = request.form.get('platform', 'Instagram')
        generated_caption = generate_caption(image_tags, requirements, caption, language, platform)
        user_caption = caption
        current_caption = generated_caption
        current_language = language
        current_platform = platform
        current_tags = image_tags
        current_requirements = requirements
        return jsonify({"caption": generated_caption}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/regenerate', methods=['POST'])
def regenerate():
    try:
        global current_caption
        index = int(request.form.get('caption-index'))
        new_caption = generate_new_caption(index)
        current_caption = new_caption
        return jsonify({"newcaption": new_caption}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate_nft', methods=['POST'])
def generate_nft():
    try:
        # Split the current_caption into individual prompts
        prompts = f"NFT anime style art: {current_tags_top[0]}, {current_tags_top[1]}"

        print(prompts)

        # Generate an image using the selected prompt and the DALL-E API
        image_response = openai.Image.create(
            prompt=prompts,
            n=1,
            size="256x256",
        )

        # Get the URL of the generated image
        image_url = image_response["data"][0]["url"]

        # Return the image URL
        return jsonify({"image_url": image_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
