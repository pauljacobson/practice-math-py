import openai

def setup_openai_api():
    openai.api_key = 'YOUR_API_KEY'

def ask_openai(question):
    setup_openai_api()
    response = openai.Completion.create(
      engine="davinci",
      prompt=question,
      max_tokens=150
    )
    return response.choices[0].text
