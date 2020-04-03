from django.core.management.base import BaseCommand, CommandError
from book.models import Book, Rating
from django.contrib.auth.models import User
from django.utils import timezone

import random    

class Command(BaseCommand):
    help = "Adjust Book Rating"

    def handle(self, *args, **options):
        add_rating()


def add_rating():
    book_list = list(Book.objects.all())
    all_user_list = list(User.objects.filter(is_staff=False))
    random.shuffle(book_list)
    N = len(book_list)
    for i in range(N):
        print(i)
        book = book_list[i]
        no_rating = random.randint(60, 100)
        user_list = random.sample(all_user_list, no_rating)
        if i< int(0.1*N):    
            for i in range(len(user_list)):
                user = user_list[i]
                if i < int(0.9*len(user_list)):
                    Rating.objects.create(
                        rating=random.randint(0,1), book=book,
                        user=user, time=timezone.now()
                    )
                else:
                    Rating.objects.create(
                        rating=random.choice([2,3,4,5]), book=book,
                        user=user, time=timezone.now()
                    )
        elif i< int(0.3*N):    
            for i in range(len(user_list)):
                user = user_list[i]
                if i < int(0.9*len(user_list)):
                    Rating.objects.create(
                        rating=random.randint(1,2), book=book,
                        user=user, time=timezone.now()
                    )
                else:
                    Rating.objects.create(
                        rating=random.choice([0,3,4,5]), book=book,
                        user=user, time=timezone.now()
                    )
        elif i< int(0.55*N):    
            for i in range(len(user_list)):
                user = user_list[i]
                if i < int(0.9*len(user_list)):
                    Rating.objects.create(
                        rating=random.randint(2,3), book=book,
                        user=user, time=timezone.now()
                    )
                else:
                    Rating.objects.create(
                        rating=random.choice([0,1,4,5]), book=book,
                        user=user, time=timezone.now()
                    )
        elif i< int(0.8*N):    
            for i in range(len(user_list)):
                user = user_list[i]
                if i < int(0.9*len(user_list)):
                    Rating.objects.create(
                        rating=random.randint(3,4), book=book,
                        user=user, time=timezone.now()
                    )
                else:
                    Rating.objects.create(
                        rating=random.choice([0,1,2,5]), book=book,
                        user=user, time=timezone.now()
                    )
        else:
            for i in range(len(user_list)):
                user = user_list[i]
                if i < int(0.9*len(user_list)):
                    Rating.objects.create(
                        rating=random.randint(4,5), book=book,
                        user=user, time=timezone.now()
                    )
                else:
                    Rating.objects.create(
                        rating=random.choice([0,1,2,3]), book=book,
                        user=user, time=timezone.now()
                    )