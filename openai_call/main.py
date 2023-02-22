import logging
import azure.functions as func

from . import search
from . import chatgpt

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting Azure functions call for ChatGPT')

    # Extract the question that is passed in
    logging.debug('Extracting question from API body')
    
    question = req.params.get('question', None)
    if not question:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            question = req_body.get('question', None)
    
    # Returns 406 error if no suitable question is supplied
    if not question:
        return func.HttpResponse(
            """No suitable question supplied. Please provide the input in the form; {"question": <input>}""",
            status_code=406
        )
    
    # Mock up the response from search. TODO: Replace with correct functionality
    search_response = search.simulate_search_response(question)
    
    # Generate chatGPT prompt
    prompt = chatgpt.generate_chatgpt_prompt(question, search_response)
    
    # Query chatGPT
    chatgpt_response = chatgpt.query_chat_gpt(prompt)
    if not question:
        return func.HttpResponse(
            "Unsuccessful query to chatGPT",
            status_code=400
        )
    
    # If everything is successful return chatGPT response
    return func.HttpResponse(
        chatgpt_response,
        status_code=200
    )