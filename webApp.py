import openai
from flask import Flask, request, jsonify, render_template

openai.api_key = "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"

app = Flask(__name__)

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
    return response.choices[0].text.strip()

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

        output_text = generate_blog_post(input_text, style, platform)
        print(output_text)
        return jsonify({"output_text": output_text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
