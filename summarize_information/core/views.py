import os
import json
import hashlib
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics import ExtractSummaryAction
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Text

load_dotenv()

AZURE_API_KEY = os.getenv('AZURE_API_KEY')
AZURE_API_ENDPOINT = "https://cloud-computing.cognitiveservices.azure.com/"

@csrf_exempt
def index(request):
    client = authenticate_client()
    unsummarized_text = request.POST.get('unsummarized_text', '')
    summarized_text = ''
    if unsummarized_text:
        if not input_exists(hash_unsummarized(unsummarized_text)):
            summarized_text = sample_extractive_summarization(client, unsummarized_text)
            Text.objects.create(input_text=hash_unsummarized(unsummarized_text), output_text=summarized_text)
        else:
            summarized_text = get_output_if_exists(hash_unsummarized(unsummarized_text))
    return render(request, 'core/index.html', {'unsummarized_text': unsummarized_text, 'summarized_text': summarized_text})

def authenticate_client():
    ta_credential = AzureKeyCredential(AZURE_API_KEY)
    text_analytics_client = TextAnalyticsClient(endpoint=AZURE_API_ENDPOINT, credential=ta_credential)
    return text_analytics_client

def sample_extractive_summarization(client, input_text):
    document = [input_text]
    poller = client.begin_analyze_actions(document, actions=[ExtractSummaryAction(max_sentence_count=4)])
    document_results = poller.result()
    output_text = ''
    for result in document_results:
        extract_summary_result = result[0]
        if not extract_summary_result.is_error:
            output_text = ''.join([sentence.text for sentence in extract_summary_result.sentences])

    return output_text

def hash_unsummarized(unsummarized):
    hash_object = hashlib.sha256()
    hash_object.update(unsummarized.encode())
    hashed_unsummarized = hash_object.hexdigest()
    return hashed_unsummarized

def input_exists(text):
    return Text.objects.filter(input_text=text).exists()

def get_output_if_exists(text):
    try:
        output_text = Text.objects.get(input_text=text).output_text
        return output_text
    except Text.DoesNotExist:
        return None