from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, CommentAPIView, RatingAPIView, RecommendAPIView

router = DefaultRouter()
router.register(r'', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<id>/comment/', CommentAPIView.as_view(), name="comment"),
    path('<id>/rating/', RatingAPIView.as_view(), name="rating"),
    path('get/recommend/', RecommendAPIView.as_view(), name="recommend"),
]