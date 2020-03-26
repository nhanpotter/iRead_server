from rest_framework import serializers

from djoser.serializers import UserSerializer

from .models import *

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    overall_rating = serializers.FloatField()

    class Meta:
        model = Book
        fields = '__all__'

class CommentSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    book = serializers.PrimaryKeyRelatedField(read_only=True)
    comment = serializers.CharField()
    time = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        created = Comment(**validated_data)
        created.save()
        return created

    def update(self, instance, validated_data):
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance

class RatingSerializer(serializers.Serializer):
    book = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.IntegerField()

    def create(self, validated_data):
        created = Rating(**validated_data)
        created.save()
        return created

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance