from django.urls import path
from .views import PredictionView, WeeklyStatsAPIView, MonthlyStatsAPIView

urlpatterns = [
    path('predict/', PredictionView.as_view(), name='predict'),
    path('predict', PredictionView.as_view(), name='predict'),
    path('weeklystats/', WeeklyStatsAPIView.as_view(), name='weeklystats'),
    path('weeklystats', WeeklyStatsAPIView.as_view(), name='weeklystats'),
    path('monthlystats/', MonthlyStatsAPIView.as_view(), name='monthlystats'),
    path('monthlystats', MonthlyStatsAPIView.as_view(), name='monthlystats'),
]