from django.core.management.base import BaseCommand, CommandError
from book.models import Book, Rating

import random

class Command(BaseCommand):
    help = "Adjust Book Rating"

    def add_arguments(self, parser):
        parser.add_argument('no_book', type=int, help="Number of books to change")
        parser.add_argument('percent', type=int, help="Percentage of ratings to be changed")
        parser.add_argument('from', type=int, help="Final Rating is from this number")
        parser.add_argument('to', type=int, help="Final Rating is to this number")

    def handle(self, *args, **options):
        no_book = options['no_book']
        percent = options['percent']
        rating_from = options['from']
        rating_to = options['to']
        
        book_list = list(Book.objects.all())
        random.shuffle(book_list)
        book_to_change = []

        for book in book_list:
            rating = book.overall_rating
            if rating >=2 and rating <= 4:
                book_to_change.append(book)
            if (len(book_to_change) >= no_book):
                break
        
        for book in book_to_change:
            print(book)
            rating_to_change = list(Rating.objects.filter(book=book))
            change_number = int(percent*len(rating_to_change)/100)
            random_list = random.sample(rating_to_change, change_number)
            for obj in random_list:
                obj.rating = random.randint(rating_from, rating_to)
                obj.save()


