from django.urls import path
from .views import PhotoUploadAPIView, PhotoRetrieveAPIView

urlpatterns = [
    path('photos/add/', PhotoUploadAPIView.as_view(), name='photo-upload'),
    path('photos/<int:photo_id>/', PhotoRetrieveAPIView.as_view(), name='photo-retrieve'),
]
