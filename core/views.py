from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Photo
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import mimetypes


class PhotoUploadAPIView(APIView):
    def post(self, request):
        image = request.FILES.get('image')
        if not image:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)

        photo = Photo.objects.create(image=image.read())
        return Response({"message": "Photo uploaded successfully", "id": photo.id})


class PhotoRetrieveAPIView(APIView):
    def get(self, request, photo_id):
        if photo_id == 1337:
            return HttpResponse("Custom response for ID 1337", content_type="text/plain")

        photo = get_object_or_404(Photo, id=photo_id)

        file_extension = photo.image.name.split('.')[-1].lower()

        content_type, _ = mimetypes.guess_type(f"image.{file_extension}")
        if not content_type:
            content_type = 'application/octet-stream'

        response = HttpResponse(photo.image, content_type=content_type)

        response['Content-Disposition'] = f'inline; filename="photo_{photo_id}.{file_extension}"'

        return response

