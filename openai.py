import os
import openai

# Set constants
openai.api_key = os.getenv("OPENAI_KEY")
model_engine = "text-davinci-003"

prompt = "Hi, how are you?"

completion = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5,
)

response = completion.choices[0].text
print(response)