import os
import json
from django.test import TestCase, Client, RequestFactory
from .models import Text
from core.views import input_exists, get_output_if_exists, load_test_phrases, index
from .views import sample_extractive_summarization, authenticate_client

class TestSummarization(TestCase):

    def setUp(self):
        self.client = authenticate_client()
        self.factory = RequestFactory()
        Text.objects.create(input_text="test input", output_text="test output")

    def test_index_view(self):
        request = self.factory.post('/', {'unsummarizedText': 'This is a test input for summarization.'})
        response = index(request)
        self.assertIn('summarizedText', response.content.decode('utf-8'))
        request = self.factory.post('/', {'unsummarizedText': 'This is a test input for summarization.'})
        response = index(request)
        self.assertIn('summarizedText', response.content.decode('utf-8'))

    def test_existing_input_text(self):
        input_text = "test input"
        expected_output = "test output"
        result = get_output_if_exists(input_text)
        self.assertEqual(result, expected_output)

    def test_nonexistent_input_text(self):
        input_text = "test none output"
        result = get_output_if_exists(input_text)
        self.assertIsNone(result)

    def test_summarization(self):
        file_path_testphrases = os.path.join(os.path.dirname(__file__), '../../testphrases.json')
        with open(file_path_testphrases) as f:
            test_phrases = json.load(f)
        input_text = test_phrases.get("test_input_phrase")
        expected_output = test_phrases.get("test_output_phrase")
        output = sample_extractive_summarization(self.client, input_text)
        self.assertEqual(output, expected_output)

    def test_load_test_phrases(self):
        expected_output = "The extractive summarization feature uses natural language processing techniques to locate key sentences in an unstructured text document.This feature is provided as an API for developers.In the public preview, extractive summarization supports several languages.It is based on pretrained multilingual transformer models, part of our quest for holistic representations."
        actual_output = load_test_phrases()
        self.assertEqual(expected_output, actual_output)

    def test_input_exists(self):
        self.assertTrue(input_exists('test input'))

    def test_input_does_not_exist(self):
        self.assertFalse(input_exists('test output'))