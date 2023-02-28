import logging
import os
import openai

def query_chat_gpt(prompt:str, model_engine="text-davinci-003", max_tokens=100) -> str:
    openai.api_key = os.getenv("OPENAI_KEY")
    
    try:
        chatgpt_response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.5,
        )
        logging.info('Successfully queried chatGPT')
        return chatgpt_response.choices[0].text
    except:
        logging.info('Unsuccesful chatGPT query')
        return None

def generate_chatgpt_prompt(question: str, search_response: str) -> str:
    prompt = f"""
        Answer the following question in 50 words or less based on the input provided and any additional information available.
        Apply more weight to responses with a higher relevance score. Note: The input is in the format 
        {{relavance score: input text}}. Question: {question}. Input: {search_response}
    """
    return prompt