import os
#import AzureTextSummary
from django.shortcuts import render
#from azure.core.credentials import AzureKeyCredential
#from azure.ai.textanalytics import (TextAnalyticsClient,ExtractSummaryAction)
from .models import Text
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == "POST":
        unsummarizedText = request.POST['unsummarizedText']
        print(unsummarizedText)
        summarizedText = "test"
        Text(input_text=unsummarizedText, output_text=summarizedText).save()
        # endpoint = os.environ["AZURE_TEXT_ANALYTICS_ENDPOINT"]
        # key = os.environ["AZURE_TEXT_ANALYTICS_KEY"]

        # text_analytics_client = TextAnalyticsClient(
        #     endpoint=endpoint,
        #     credential=AzureKeyCredential(key),
        # )

        # document = [
        #     "Document text of What you want to be summarized"
        # ]

        # poller = text_analytics_client.begin_analyze_actions(
        #     document,
        #     actions=[
        #         ExtractSummaryAction(),
        #     ],
        # )

        # document_results = poller.result()
        # for result in document_results:
        #     extract_summary_result = result[0]  # first document, first result
        #     print("Summary extracted: \n{}".format(" ".join([sentence.text for sentence in extract_summary_result.sentences])))

        
        
    return render(request, 'core/index.html', {})