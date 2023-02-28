import logging
import os
import json
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
#from azure.search.documents import Highlight

def simulate_search_response(question: str):
    logging.info('Simulating search response')
    return {"Test Document": "The population of Australia is 26 million"}


class AzureSearchClient:

    def __init__(self, search_service_name, index_name):
        api_key = os.environ.get("SEARCH_KEY")
        print(f"the api key is {api_key}")
        self.search_service_name = search_service_name
        self.index_name = index_name
        self.api_key = api_key
        self.search_client = SearchClient(
            endpoint=f"https://{search_service_name}.search.windows.net",
            index_name=index_name,
            credential=AzureKeyCredential(api_key))

    def refine_search(self, search_query: str) -> str:
        #https://azuresdkdocs.blob.core.windows.net/$web/python/azure-search-documents/11.4.0b1/azure.search.documents.html
        request = self.search_client.search(search_text=search_query
                                            ,query_type = "semantic"
                                            ,semantic_configuration_name = "badjuju"
                                            ,query_language = "en-us" #needs to be US English for spell check to work
                                            ,query_speller = "lexicon"
                                            ,query_caption = "extractive"
                                            ,query_answer = "extractive|count-3") 
        # Inialise the search request instance
        # Set the query type, types are "full" or "simple" or "semantic"
        # Set the semantic configuration, this is a custom configuration that we can define in the Azure portal
        # Set the speller, this is a custom configuration that we can define in the Azure portal
        return request
    
    def prep_results_chatgpt(self, response: dict, max_values: int) -> str:
        # Get all results from the search response
        #search_results = json.loads(search_response)
        count = 0
        items = {}
        for result in response:
            for key, value in result.items():
                if key == '@search.reranker_score':
                    score = value
                elif key == '@search.captions':
                    for caption in value:
                        key_text = caption.text
                        items[score] = key_text
                        count += 1
                else:
                    pass
            if count == max_values:
                break
        return items

            