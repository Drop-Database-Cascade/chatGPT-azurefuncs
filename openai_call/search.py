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
        request = self.search_client.search(search_text=search_query) # Inialise the search request instance
        request.query_type = "semantic" # Set the query type, types are "full" or "simple" or "semantic"
        request.semanticConfiguration = "semantictest" # Set the semantic configuration, this is a custom configuration that we can define in the Azure portal
        #request.scoring_parameters = ["relevance"] # define how results are ranked, in this case we are using relevance
        #request.top = 5 # Set the number of results to return
        #request.cutoff_frequency = 0.5 # Exclude terms that appear in more than 50% of the documents - possible refinement
        #request.search_fields = ["content"] # Set the search fields, we can use this as a possible refinement - by defualt all fields are searched
        #request.filter = "content eq 'Australia'" # Filter the results to only include documents that contain the word "Australia" - possible refinement
        #request.scoring_profile = "my-profile" # Set the scoring profile, this is a custom profile that we can define in the Azure portal - possible refinement
        #highlight = Highlight(pre_tag='<b>', post_tag='</b>', fields=['content'])
        #request.highlight = highlight - possible refinement
        return request
        
    def get_response_cog_search(self, search_query: str) -> dict:
        response = self.search_client.search(search_query)
        items = []

        page = response.next()

        while page is not None:
            for result in page:
                items.append(result)
            page = response.next()
       
        json_string = json.dumps(items)
        response = json.loads(json_string)
        print(response)
        return response
    
    def prep_results_chatgpt(self, search_response: dict, max_values: int) -> str:
        # Get all results from the search response
        #search_results = json.loads(search_response)

        # Loop through response and get the key text and reranker score
        count = 0
        max_values
        outputdict = {}
        for item in search_response["value"]:
            reranker_score = item["@search.rerankerScore"]
            for caption in item["@search.captions"]:
                key_text = caption["text"]
                outputdict[reranker_score] = key_text
                count += 1
                if count == max_values:
                    break
            if count == max_values:
                break

        return str(outputdict)


