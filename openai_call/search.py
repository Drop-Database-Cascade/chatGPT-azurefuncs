import logging
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import Highlight

def simulate_search_response(question: str):
    logging.info('Simulating search response')
    return {"Test Document": "The population of Australia is 26 million"}


class AzureSearchClient:

    def __init__(self, search_service_name, index_name):
        api_key = os.environ.get("AZURE_SEARCH_KEY")
        self.search_service_name = search_service_name
        self.index_name = index_name
        self.api_key = api_key
        self.search_client = SearchClient(
            endpoint=f"https://{search_service_name}.search.windows.net",
            index_name=index_name,
            credential=AzureKeyCredential(api_key))

    def refine_search(self, search_query: str) -> str:
        request = self.search_client.search.search_request() # Inialise the search request instance
        request.search_text = search_query # Set the search text
        request.query_type = "simple" # Set the query type, types are "full" or "simple" or "semantic"
        request.scoring_parameters = ["relevance"] # define how results are ranked, in this case we are using relevance
        request.top = 5 # Set the number of results to return
        #request.cutoff_frequency = 0.5 # Exclude terms that appear in more than 50% of the documents - possible refinement
        #request.search_fields = ["content"] # Set the search fields, we can use this as a possible refinement - by defualt all fields are searched
        #request.filter = "content eq 'Australia'" # Filter the results to only include documents that contain the word "Australia" - possible refinement
        #request.scoring_profile = "my-profile" # Set the scoring profile, this is a custom profile that we can define in the Azure portal - possible refinement
        #highlight = Highlight(pre_tag='<b>', post_tag='</b>', fields=['content'])
        #request.highlight = highlight - possible refinement
        return request
        
    def get_response_cog_search(self, search_query: str) -> dict:
        response = self.search_client.search(search_query)
        print(response)
        return response
    
    def prep_results_chatgpt(self, search_response: dict, char_lim: int) -> str:
        # Get the top 3 results from the search response
        sorted_results = sorted(search_response, key=lambda x: x["@search.score"], reverse=True)
        top_results = sorted_results[:3]

        # Get response text from the top 3 results
        top_texts = [result["content"] for result in top_results]
        full_text = "\n\n".join(top_texts)
        # trim to chat gpt fit
        trimmed_text = full_text[:char_lim]

        return trimmed_text


