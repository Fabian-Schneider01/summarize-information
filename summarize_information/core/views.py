import os
import json

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics import ExtractSummaryAction
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Text

def load_test_phrases():
    file_path_testphrases = os.path.join(os.path.dirname(__file__), '../../testphrases.json')
    with open(file_path_testphrases) as f:
        test_phrases = json.load(f)
    return test_phrases

# Read Azure API key and endpoint from json file
file_path = os.path.join(os.path.dirname(__file__), '../../keys.json')
with open(file_path) as f:
    data = json.load(f)

AZURE_API_KEY = data["api_keys"][0]["API_KEY"]
AZURE_API_ENDPOINT = data['api_keys'][0]['API_ENDPOINT']

@csrf_exempt
def index(request):
    # Authenticate client
    client = authenticate_client()

    # Get text input from user and retrieve summarized text
    unsummarized_text = request.POST.get('unsummarizedText', '')
    summarized_text = ''

    if unsummarized_text:
        if not input_exists(unsummarized_text):
            summarizedText = sample_extractive_summarization(client, unsummarized_text)
            Text.objects.create(input_text=unsummarized_text, output_text=summarizedText)
        else:
            summarizedText = get_output_if_exists(unsummarized_text)

    return render(request, 'core/index.html', {'unsummarizedText': unsummarized_text, 'summarizedText': summarized_text})


# Check if input already exists in the database
def input_exists(text):
    return Text.objects.filter(input_text=text).exists()


# If output exists, get the entry from the database
def get_output_if_exists(text):
    try:
        output_text = Text.objects.get(input_text=text).output_text
        return output_text
    except Text.DoesNotExist:
        return None


# Authenticate the client for Azure Text Analytics service
def authenticate_client():
    ta_credential = AzureKeyCredential(AZURE_API_KEY)
    text_analytics_client = TextAnalyticsClient(
        endpoint=AZURE_API_ENDPOINT,
        credential=ta_credential)
    return text_analytics_client


# Analyze the text using Azure Text Analytics service
def sample_extractive_summarization(client, input_text):
    document = [input_text]
    poller = client.begin_analyze_actions(
        document,
        actions=[
            ExtractSummaryAction(max_sentence_count=4)
        ],
    )
    document_results = poller.result()

    # Create output text
    output_text = ''
    for result in document_results:
        extract_summary_result = result[0]
        if not extract_summary_result.is_error:
            output_text = ''.join([sentence.text for sentence in extract_summary_result.sentences])

    return output_text

