from django.db import models
from django.contrib.auth.models import User

from .utils import check_valid_year

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    def __unicode__(self):
        return self.name

class Book(models.Model):
    # Base information
    uid = models.CharField(max_length=255)
    book_title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    summary = models.TextField()
    original_publisher = models.CharField(max_length=255)
    digital_publisher = models.CharField(max_length=255)
    item_format = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    item_copyright = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    published = models.CharField(max_length=255, null=True)
    resource_url = models.CharField(max_length=255)
    cover = models.CharField(max_length=255)
    thumbnail = models.CharField(max_length=255)

    # Additional Info
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.book_title

    def __unicode__(self):
        return self.book_title

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
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    rating = models.IntegerField()

    # Mapping
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book', 'user'], name='unique user rating')
        ]


