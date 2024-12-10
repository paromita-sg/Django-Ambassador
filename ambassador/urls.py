from django.urls import path, include

from .views import ProductBackendAPIView, ProductFrontendAPIView, LinkAPIView, StatsApiView, RankingAPIView

urlpatterns = [
    path('', include('common.urls')),
    path('products/frontend', ProductFrontendAPIView.as_view()),
    path('products/backend', ProductBackendAPIView.as_view()),
    path('links', LinkAPIView.as_view()),
    path('stats', StatsApiView.as_view()),
    path('rankings', RankingAPIView.as_view()),
]
