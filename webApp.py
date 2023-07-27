import openai
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

openai.api_key = "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"

app = Flask(__name__)
CORS(app, supports_credentials=True)

def generate_blog_post(input_text, style, platform):
    # Use GPT-3.5 to generate the improved output
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.8,
        max_tokens=2000,
        messages=[
            {"role": "system", "content": f"You are writing a {style} blog post for {platform}."},
            {"role": "user", "content": input_text}
        ]
    )
    print(response.choices[0].message["content"])
    return response.choices[0].message["content"]

def generate_test_post(input_text, style, platform):
    response = "This is a test output."
    return response

@app.route('/')
def index():
    return render_template('blogApp.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        input_text = data['input_text']
        style = data['style']
        platform = data['platform']

        if not input_text or not style or not platform:
            return jsonify({"error": "Please provide input text, style, and platform."}), 400

        # output_text = generate_blog_post(input_text, style, platform)
        output_text = generate_test_post(input_text, style, platform)
        return jsonify({"output_text": output_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
