from django.db import models
from django.contrib.auth.models import User

from .utils import check_valid_year
from django.utils import timezone
import pickle

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

class Book(models.Model):
    # Base information
    uid = models.CharField(max_length=500, unique=True)
    book_title = models.CharField(max_length=500)
    subject = models.CharField(max_length=500)
    summary = models.TextField()
    original_publisher = models.CharField(max_length=500)
    digital_publisher = models.CharField(max_length=500)
    item_format = models.CharField(max_length=500)
    language = models.CharField(max_length=500)
    item_copyright = models.CharField(max_length=500)
    author_name = models.CharField(max_length=500)
    published = models.CharField(max_length=500, null=True)
    resource_url = models.CharField(max_length=2048)
    cover = models.CharField(max_length=2048)
    thumbnail = models.CharField(max_length=2048)

    # Additional Info
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "Title: {0} - Genre: {1}".format(self.book_title, self.genre.name)

    def __unicode__(self):
        return "Title: {0} - Genre: {1}".format(self.book_title, self.genre.name)

    def clean(self):
        if self.published is None or not check_valid_year(self.published):
            self.published = None
            self.save()

    # Attribute
    def get_overall_rating(self):
        rating_list = self.rating_set.all()
        n = len(rating_list)
        if n==0:
            return None

        overall = 0
        for rating in rating_list:
            overall += rating.rating
        
        return overall/n

    overall_rating = property(get_overall_rating)

    
class Comment(models.Model):
    comment = models.TextField()
    time = models.DateTimeField()

    # Mapping
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class Rating(models.Model):
    RATING_CHOICES = [
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    rating = models.IntegerField(choices=RATING_CHOICES)
    time = models.DateTimeField()

    # Mapping
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book', 'user'], name='unique user rating')
        ]

class MachineLearning(models.Model):
    _value = models.BinaryField()

    def set_data(self, data):
        self._value = pickle.dumps(data)

    def get_data(self):
        return pickle.loads(self._value)

    value = property(get_data, set_data)
    
