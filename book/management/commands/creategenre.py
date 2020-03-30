from django.core.management.base import BaseCommand, CommandError
from book.models import Genre

def create_genre():
    genre_list = ["Fantasy", "Adventure", "Romance", "Mystery", "Horror", "Science Fiction", "Humor"]
    for genre in genre_list:
        Genre.objects.create(name=genre)
        print("Genre {0} created".format(genre))

class Command(BaseCommand):
    help = "Create Genre"

    def handle(self, *args, **options):
        create_genre()