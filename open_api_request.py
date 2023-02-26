# Note this file is just an example copied from Chat GPT

import logging
import requests
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    question = req.params.get('question')
    if not question:
        try:
            req_body = req.get_json()
        
        except ValueError:
            return func.HttpResponse(
                "Please provide a question in the query string.",
                status_code=400
            )
        else:
            question = req_body.get('question')

    print(question)

    # Set up the API request
    api_key = 'your_openai_api_key_here'
    url = 'https://api.openai.com/v1/completions'
    prompt = f"Answer the following question: {question}\nAnswer:"
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {api_key}'}
    data = {'prompt': prompt,
            'temperature': 0.5,
            'max_tokens': 1024,
            'n': 1,
            'stop': ''}

    # Send the API request and extract the answer
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    answer = response_data['choices'][0]['text']

    return func.HttpResponse(f"The answer to your question is: {answer}")

# Example https://your-function-url.azurewebsites.net/api/your-function-name?question=What%20is%20the%20capital%20of%20France%3F