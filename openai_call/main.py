import logging
import azure.functions as func
import os
from . import search
from . import chatgpt
#from search import AzureSearchClient as ASC

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting Azure functions call for ChatGPT')

    # Extract the question that is passed in
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
        logging.info(f"No valid question supplied")
        return func.HttpResponse(
            """No suitable question supplied. Please provide the input in the form; {"question": <input>}""",
            status_code=406
        )
    
    # Log the question
    logging.info(f"User question is: {question}")
    
    # Mock up the response from search. TODO: Replace with correct functionality
    #search_response = search.simulate_search_response(question)

    # Initialize Azure Search Client
    search_client = search.AzureSearchClient("searchisnow", "document-index")

    # Refine & send search request with Azure Search Config
    srequest = search_client.refine_search(question)
    logging.info(f"Refined search request paramaters are: {srequest}")

    # Add logic to prep output for chatGPT
    cleaned_response = search_client.prep_results_chatgpt(srequest, 5)
    logging.info(cleaned_response)

    # Generate chatGPT prompt
    prompt = chatgpt.generate_chatgpt_prompt(question, cleaned_response)
    logging.info(f"ChatGPT prompt is: {prompt}")
    
    # Query chatGPT
    chatgpt_response = chatgpt.query_chat_gpt(prompt)
    if not question:
        return func.HttpResponse(
            "Unsuccessful query to chatGPT",
            status_code=400
        )
    
    # If everything is successful return chatGPT response
    logging.info("Chat GPT Function call successful")
    return func.HttpResponse(
        chatgpt_response,
        status_code=200
    )