import os
import json
from .models import Text
from django.shortcuts import render
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics import ExtractSummaryAction
from django.views.decorators.csrf import csrf_exempt

#read api key and endpoint from json file
file_path = os.path.join(os.path.dirname(__file__), '../../keys.json')
with open(file_path) as f:
    data = json.load(f)

AZURE_API_KEY = data["api_keys"][0]["API_KEY"]
AZURE_API_ENDPOINT = data['api_keys'][0]['API_ENDPOINT']

@csrf_exempt
def index(request):
    client = authenticate_client()
    # text to be summarized
    unsummarizedText = ""
    summarizedText = ""
    if request.method == "POST":
        # get input text 
        unsummarizedText = request.POST['unsummarizedText']
        # check if the request already exists
        if not inputExists(unsummarizedText): #not existing => make api request
            summarizedText = sample_extractive_summarization(client, unsummarizedText)
            # save input and output in database for efficency if same input is used again
            Text(input_text=unsummarizedText, output_text=summarizedText).save()
        else:
            # already exists => read output from database
            saved_texts = getOutputIfExists(unsummarizedText)
            return render(request, 'core/index.html', {'unsummarizedText': saved_texts.get('input_text'), 'summarizedText': saved_texts.get('output_text')})

    for i in loadTestPhrases():
        print(i)
    
    return render(request, 'core/index.html', {'unsummarizedText': unsummarizedText, 'summarizedText': summarizedText})

# checking if input already exists in database
def inputExists(text):
    return Text.objects.filter(input_text=text).exists()

# if output exists, get the entry in database
def getOutputIfExists(text):
    try:
        output_text = Text.objects.get(input_text=text).output_text
        return {"output_text": output_text, "input_text": text}
    except Text.DoesNotExist:
        return None

# authentification for service
def authenticate_client():
    ta_credential = AzureKeyCredential(AZURE_API_KEY)
    text_analytics_client = TextAnalyticsClient(
            endpoint=AZURE_API_ENDPOINT, 
            credential=ta_credential)
    return text_analytics_client

# analyzing the text 
def sample_extractive_summarization(client, input_text):
    text=""
    document = [
        input_text
    ]

    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(max_sentence_count=4)
        ],
    )

    document_results = poller.result()

    # create output text
    for result in document_results:
        extract_summary_result = result[0] 
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            text = text.join([sentence.text for sentence in extract_summary_result.sentences])
    return text

def loadTestPhrases():
    file_path_testphrases = os.path.join(os.path.dirname(__file__), '../../testphrases.json')
    with open(file_path_testphrases) as f:
        test_phrases = json.load(f)
    return test_phrases["test_phrases"]



