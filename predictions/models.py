from django.db import models


class Prediction(models.Model):
    result = models.CharField(max_length=100)
    created_at = models.DateTimeField()

    class Meta:
        db_table = "predictions"
