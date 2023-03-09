import os
import json
from .models import Text
from django.shortcuts import render
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics import ExtractSummaryAction
from django.views.decorators.csrf import csrf_exempt

file_path = os.path.join(os.path.dirname(__file__), '../../keys.json')
with open(file_path) as f:
    data = json.load(f)

AZURE_API_KEY = data["api_keys"][0]["API_KEY"]
AZURE_API_ENDPOINT = data['api_keys'][0]['API_ENDPOINT']

@csrf_exempt
def index(request):
    client = authenticate_client()
    summarizedText = ""
    if request.method == "POST":
        unsummarizedText = request.POST['unsummarizedText']
        if not inputExists(unsummarizedText):
            summarizedText = sample_extractive_summarization(client, unsummarizedText)
            Text(input_text=unsummarizedText, output_text=summarizedText).save()
        else:
            summarizedText = getOutputIfExists(unsummarizedText)
            print("Already exists")
    
    print("this is summarized: ", summarizedText)
    return render(request, 'core/index.html', {'summarizedText': summarizedText})

def inputExists(text):
    return Text.objects.filter(input_text=text).exists()

def getOutputIfExists(text):
    try:
        text = Text.objects.get(input_text=text)
        return text.output_text
    except Text.DoesNotExist:
        return None

def authenticate_client():
    ta_credential = AzureKeyCredential(AZURE_API_KEY)
    text_analytics_client = TextAnalyticsClient(
            endpoint=AZURE_API_KEY, 
            credential=ta_credential)
    return text_analytics_client

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
    for result in document_results:
        extract_summary_result = result[0] 
        if extract_summary_result.is_error:
            print("...Is an error with code '{}' and message '{}'".format(
                extract_summary_result.code, extract_summary_result.message
            ))
        else:
            text = text.join([sentence.text for sentence in extract_summary_result.sentences])
    return text