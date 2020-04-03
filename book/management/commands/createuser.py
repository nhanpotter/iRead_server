import random

from django.core.management.base import BaseCommand, CommandError
from book.models import Rating, Book
from django.contrib.auth.models import User
from django.utils import timezone

class Command(BaseCommand):
    """
    Note: Disable signal before running this
    """
    help = "Create Unreal Users"

    def add_arguments(self, parser):
        parser.add_argument('number_of_users', nargs='+', type=int)

    def handle(self, *args, **options):
        number_of_users = options['number_of_users'][0]
        base_username = "student"
        # book_list = list(Book.objects.all())
        for i in range(1, number_of_users+1):
            try:
                # Create new user
                username = base_username+str(i)
                email = 'example{0}@example.com'.format(str(i))
                new_user = User.objects.create(
                    username=username, email=email,
                    is_active=True
                )
                new_user.set_password(str(i))
                new_user.save()
                print('User {0} created'.format(str(i)))
                # # Shuffle Book List and Create Random Rating
                # random.shuffle(book_list)
                # for j in range(random.randint(3, 20)):
                #     new_rating = random.choice(Rating.RATING_CHOICES)[0]
                #     Rating.objects.create(
                #         rating=new_rating, book=book_list[j], 
                #         user=new_user, time=timezone.now()
                    # )
                
            except:
                print('Creating Failed')
                continue