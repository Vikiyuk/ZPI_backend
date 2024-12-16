from django.http import JsonResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from django.db import models
from .models import Prediction

MODEL_PATH = "predictions/skin_cancer_model.h5"

model = load_model(MODEL_PATH)
classes = ["nevus", "melanoma", "basal cell carcinoma"]


class PredictionView(APIView):
    def post(self, request):
        uploaded_file = request.FILES.get("image")
        if not uploaded_file:
            return JsonResponse({"error": "No image provided"}, status=400)

        print(f"Received file: {uploaded_file.name}")

        try:
            # Przetwarzanie obrazu
            image = Image.open(uploaded_file)
            image = image.resize((224, 224))
            image_array = img_to_array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            print("Image prepared for prediction.")

            # Predykcja
            predictions = model.predict(image_array)[0]
            predictions_percent = [round(prob * 100) for prob in predictions]
            results = {cls: prob for cls, prob in zip(classes, predictions_percent)}
            print("Predictions made.")

            # Wybór klasy z największą szansą
            max_class_index = np.argmax(predictions)
            predicted_disease = classes[max_class_index]
            print(f"Predicted disease: {predicted_disease}")

            # Zapis w bazie danych
            Prediction.objects.create(
                result=predicted_disease,
                created_at=timezone.now()
            )
            print("Prediction saved to the database.")

            return JsonResponse({"predictions": results}, status=200)

        except Exception as e:
            print(f"Error processing file: {e}")
            return JsonResponse({"error": str(e)}, status=500)


class WeeklyStatsAPIView(APIView):
    def get(self, request):
        week_ago = timezone.now() - timedelta(days=7)

        stats = (
            Prediction.objects.filter(created_at__gte=week_ago)
            .values('result')
            .annotate(count=models.Count('result'))
            .order_by('result')
        )

        # Return the result
        return Response(stats)


class MonthlyStatsAPIView(APIView):
    def get(self, request):
        month_ago = timezone.now() - timedelta(days=30)

        stats = (
            Prediction.objects.filter(created_at__gte=month_ago)
            .values('result')
            .annotate(count=models.Count('result'))
            .order_by('result')
        )

        return Response(stats)

