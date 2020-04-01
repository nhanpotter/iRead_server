from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from djoser.serializers import UserSerializer

from .serializers import BookSerializer, CommentSerializer, RatingSerializer
from .models import *

# Create your views here.

class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class CommentAPIView(APIView): 
    def get(self, request, id, format=None):
        comments = Comment.objects.filter(book__id=id)
        # Order by most recent
        comments = comments.order_by('-time')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            book = Book.objects.get(id=id)
            serializer.save(user=request.user, book=book, time=timezone.now())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingAPIView(APIView):
    def get(self, request, id, format=None):
        try:
            rating = Rating.objects.get(user=request.user, book__id=id)
            serializer = RatingSerializer(rating)

            return Response(serializer.data)
        except Rating.DoesNotExist:
            return Response(
                {'rating': ['You have not rated this book yet']},
                status=status.HTTP_200_OK
            )
        
    def post(self, request, id, format=None):
        try:
            rating = Rating.objects.get(user=request.user, book__id=id)
        except Rating.DoesNotExist:
            rating = None

        if rating is None:
            serializer = RatingSerializer(data=request.data)
        else:
            serializer = RatingSerializer(rating, data=request.data)
        if serializer.is_valid():
            book = Book.objects.get(id=id)
            serializer.save(user=request.user, book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecommendAPIView(APIView):
    def get(self, request, format=None):
        user = request.user
        if user.is_staff:
            return Response(
                {'error': ['Admin cannot have recommendations']},
                status=status.HTTP_204_NO_CONTENT
            )

        ml_obj = MachineLearning.objects.first().value
        rec_model = ml_obj["model"]
        data_fit = ml_obj["data"]
        user_id = user.id
        user_mapping = data_fit.get_user_mapping()
        book_mapping = data_fit.get_book_mapping()
        recommend_list = rec_model.recommend_user(user_id, user_mapping, book_mapping)
        serializer = BookSerializer(recommend_list, many=True)
        return Response(serializer.data)