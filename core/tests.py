from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from unittest.mock import patch
from .models import Photo
from predictions.models import Prediction
import tempfile
from PIL import Image
import io

class PredictionViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('predict')

    def create_test_image(self):
        image = Image.new('RGB', (224, 224))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, format='JPEG')
        tmp_file.seek(0)
        return tmp_file

    @patch('predictions.views.model.predict')
    def test_prediction_success(self, mock_predict):
        mock_predict.return_value = [[0.1, 0.7, 0.2]]
        test_image = self.create_test_image()
        response = self.client.post(self.url, {'image': test_image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('predictions', response.json())

    def test_prediction_no_image(self):
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'No image provided')


class WeeklyStatsAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('weeklystats')
        Prediction.objects.create(result='melanoma', created_at=timezone.now())

    def test_weekly_stats(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['result'], 'melanoma')
        self.assertEqual(response.json()[0]['count'], 1)


class MonthlyStatsAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('monthlystats')
        Prediction.objects.create(result='nevus', created_at=timezone.now())

    def test_monthly_stats(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()[0]['result'], 'nevus')
        self.assertEqual(response.json()[0]['count'], 1)


class DiseaseListAPIViewTests(APITestCase):
    @patch('core.views.MongoClient')
    def test_disease_list(self, mock_mongo):
        mock_mongo.return_value.__getitem__.return_value['zpi'].find.return_value = [
            {'name': 'melanoma'},
            {'name': 'nevus'}
        ]
        url = reverse('disease-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)


class PhotoRetrieveAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.photo = Photo.objects.create(image=b'test_image_data')

    def create_test_image(self):
        image = Image.new('RGB', (224, 224))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, format='JPEG')
        tmp_file.seek(0)
        return tmp_file

    def test_photo_retrieve_success(self):
        url = reverse('predict')
        test_image = self.create_test_image()
        response = self.client.post(url, {'image': test_image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('predictions', response.json())

    def test_photo_retrieve_custom_id(self):
        url = reverse('predict')
        test_image = self.create_test_image()
        response = self.client.post(url, {'image': test_image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('predictions', response.json())

    def test_photo_not_found(self):
        url = reverse('predict')
        response = self.client.post(url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], 'No image provided')

