import openai

openai.api_key = "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"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  temperature=0.8,
  max_tokens=2000,
  messages=[
    {"role": "system", "content": f"You are writing a informal blog post for instagram."},
    {"role": "user", "content": "melbourne is the most livable city"}
  ]
)

print(response.choices[0].message)