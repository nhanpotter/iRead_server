from lightfm.data import Dataset
from lightfm import LightFM
from lightfm.evaluation import precision_at_k, recall_at_k, auc_score
from lightfm.cross_validation import random_train_test_split
import time, random
import pandas as pd
from django.utils import timezone

from django.core.management.base import BaseCommand, CommandError
from book.models import Book, Rating, MachineLearning
from django.contrib.auth.models import User

class DataPrep:
    @staticmethod
    def get_user_list():
        return User.objects.filter(is_staff=False).values_list('id', flat=True)

    @staticmethod
    def get_book_obj_list():
        return Book.objects.values_list('id', 'genre__id')

    @staticmethod
    def get_book_list():
        book_obj_list = DataPrep.get_book_obj_list()
        return [x[0]-1 for x in book_obj_list]

    @staticmethod
    def get_feature_list():
        book_obj_list = DataPrep.get_book_obj_list()
        return [x[1] for x in book_obj_list]

    @staticmethod
    def get_rating_list():
        rating_list = Rating.objects.values_list('user__id', 'book__id', 'rating')
        return list(map(lambda x: (x[0], x[1]-1, x[2]), rating_list))

    @staticmethod
    def get_rating_list_from_checkpoint(checkpoint):
        rating_queryset = Rating.objects.filter(time__gte=checkpoint)
        rating_list = rating_queryset.values_list('user__id', 'book__id', 'rating')
        return list(map(lambda x: (x[0], x[1]-1, x[2]), rating_list))

    @staticmethod
    def create_features():
        book_obj_list = DataPrep.get_book_obj_list()
        return [(x[0]-1, [x[1]]) for x in book_obj_list]

    @staticmethod
    def get_readed_book_by_user(user_id):
        rating_list = list(Rating.objects.filter(user__id=user_id))
        book_list_id = [x.book.id-1 for x in rating_list]
        return book_list_id

    @staticmethod
    def get_unread_book_by_user(user_id):
        book_list_id = DataPrep.get_readed_book_by_user(user_id)
        book_queryset = Book.objects.exclude(id__in=book_list_id)
        unreaded_books = list(book_queryset.values_list('id', flat=True))
        return list(map(lambda x: x-1, unreaded_books))


class DataFit:
    def __init__(self):
        self.dataset = None

    def fit(self):
        book_list = DataPrep.get_book_list()
        book_feature_list = DataPrep.get_feature_list()
        user_list = DataPrep.get_user_list()
        self.dataset = Dataset()
        self.dataset.fit(
            users=user_list, items=book_list, item_features=book_feature_list
        )

        rating_list = DataPrep.get_rating_list()
        interactions, weights = self.dataset.build_interactions(rating_list)

        book_features = DataPrep.create_features()
        books_features = self.dataset.build_item_features(book_features)
        return interactions, weights, books_features

    def create_new_interactions(self, checkpoint):
        rating_list = DataPrep.get_rating_list_from_checkpoint(checkpoint)
        interactions, weights = self.dataset.build_interactions(rating_list)
        return interactions, weights

    @staticmethod
    def fit_evaluate(test_percentage=0.1):
        book_list = DataPrep.get_book_list()
        book_feature_list = DataPrep.get_feature_list()
        user_list = DataPrep.get_user_list()
        dataset = Dataset()
        dataset.fit(
            users=user_list, items=book_list, item_features=book_feature_list
        )

        rating_list = DataPrep.get_rating_list()
        random.shuffle(rating_list)
        rating_list_test = rating_list[:int(test_percentage*len(rating_list))]
        rating_list_train = rating_list[int(test_percentage*len(rating_list)):]
        interactions_train, weights_train = dataset.build_interactions(rating_list_train)
        interactions_test, weights_test = dataset.build_interactions(rating_list_test)

        return interactions_train, weights_train, interactions_test, weights_test

class RecModel:
    def __init__(self, checkpoint, books_features):
        self.model = LightFM(loss='warp')
        self.checkpoint = checkpoint
        self.books_features = books_features

    def set_checkpoint(self, checkpoint):
        self.checkpoint = checkpoint

    def fit(self, interactions, weights):
        self.model.fit(interactions, item_features=self.books_features, 
            sample_weight=weights, epochs=50, num_threads=2
        )

    def fit_partial(self, interactions, weights):
        self.model.fit_partial(interactions, item_features=self.books_features, 
            sample_weight=weights, epochs=50, num_threads=2
        )


    def recommend_user(self, user_id, num_prediction=12):
        unread_books = DataPrep.get_unread_book_by_user(user_id)
        book_list = DataPrep.get_book_list()

        score = self.model.predict(user_id, item_ids=unread_books, item_features=self.books_features)
        sorted_by_score = [x for _, x in sorted(zip(score, unread_books), key=lambda pair: pair[0])]

        try: 
            recommended = sorted_by_score[:num_prediction]
        except:
            recommend = sorted_by_score
        recommended_books = map(lambda book_id: Book.objects.get(id=book_id+1), recommended)

        return recommended_books


    def recommend_user_verbose(self, user_id, num_prediction=12):
        unread_books = DataPrep.get_unread_book_by_user(user_id)
        book_list = DataPrep.get_book_list()

        score = self.model.predict(user_id, item_ids=unread_books, item_features=self.books_features)
        sorted_by_score = [x for _, x in sorted(zip(score, unread_books), key=lambda pair: pair[0])]

        try: 
            recommended = sorted_by_score[:num_prediction]
        except:
            recommend = sorted_by_score
        
        readed_books = DataPrep.get_readed_book_by_user(user_id)
        print('Read Books: ')
        for book_id in readed_books:
            book_obj = Book.objects.get(id=book_id+1)
            print('\tBook Name: '+book_obj.book_title)
            print('\t\tGenre: ' + book_obj.genre.name)
            rating_obj = Rating.objects.get(book=book_id+1, user__id=user_id)
            print('\t\tOwn Rating: '+ str(rating_obj.rating))
            print('\t\tOverall Rating: '+ str(book_obj.overall_rating))
        print()

        recommended_books = map(lambda book_id: Book.objects.get(id=book_id+1), recommended)
        print('Recommend:')
        for book_obj in recommended_books:
            print('\tBook Name: '+book_obj.book_title)
            print('\t\tGenre: ' + book_obj.genre.name)
            print('\t\tOverall Rating: '+str(book_obj.overall_rating))

        return recommended_books


    def evaluate(self):
        # Data
        interactions_train, weights_train, interactions_test, weights_test = \
            DataFit.fit_evaluate()

        new_model = LightFM(loss='warp')
        new_model.fit(interactions_train, item_features=self.books_features, 
            epochs=100, num_threads=2, sample_weight=weights_train
        )
        print('Precision @k(Train): {0}'.format(precision_at_k(new_model, interactions_train).mean()))
        print('Precision @k(Test): {0}'.format(precision_at_k(new_model, interactions_test).mean()))
        print('Recall @k(Train): {0}'.format(recall_at_k(new_model, interactions_train).mean()))
        print('Recall @k(Test): {0}'.format(recall_at_k(new_model, interactions_test).mean()))
        print('Auc Score(Train): {0}'.format(auc_score(new_model, interactions_train).mean()))
        print('Auc Score(Test): {0}'.format(auc_score(new_model, interactions_test).mean()))

    

def new_train():
    dataFit = DataFit()
    (interactions, weights, books_features) = dataFit.fit()
    recModel = RecModel(timezone.now(), books_features)
    recModel.fit(interactions, weights)
    data_model_obj = {
        "data": dataFit,
        "model": recModel
    }
    MachineLearning.objects.create(value=data_model_obj)


def train():
    user_list = User.objects.filter(is_staff=False).values_list('id', flat=True)
    book_obj_list = Book.objects.values_list('id', 'genre__id')
    book_list = [x[0]-1 for x in book_obj_list]
    feature_list = [x[1] for x in book_obj_list]
    dataset = Dataset()
    dataset.fit(users=user_list, items=book_list, item_features=feature_list)

    rating_list = Rating.objects.values_list('user__id', 'book__id', 'rating')
    rating_list = list(map(lambda x: (x[0], x[1]-1, x[2]), rating_list))
    (interactions, weights) = dataset.build_interactions(rating_list)
    item_features = dataset.build_item_features([(x[0]-1, [x[1]]) for x in book_obj_list])
    model = LightFM(loss='warp')
    model.fit(interactions, item_features=item_features, sample_weight=weights, epochs=50, num_threads=2)
    print(item_features.shape)
    
    book_queryset = Book.objects.all()
    rating_user_list = list(Rating.objects.filter(user__id=10))
    print(rating_user_list)
    book_user_list = [x.book.id-1 for x in rating_user_list]
    book_queryset = book_queryset.exclude(id__in=book_user_list)

    book_list_id = list(book_queryset.values_list('id', flat=True))
    feature_list_id = list(book_queryset.values_list('genre__id', flat=True))



    ######### Get data to analyze 
    random.shuffle(rating_list)
    rating_train = rating_list[:int(len(rating_list)*0.9)]
    rating_test = rating_list[int(len(rating_list)*0.9):]
    (interactions_train, weights_train) = dataset.build_interactions(rating_train)
    (interactions_test, weights_test) = dataset.build_interactions(rating_test)
    item_features = dataset.build_item_features([(x[0]-1, [x[1]]) for x in book_obj_list])

    model = LightFM(loss='warp')
    records = []
    for i in range(1, 200):
        print("Training at epoch "+str(i))
        record = []
        record.append(i)
        start_time = time.time()
        model.fit(interactions_train, item_features=item_features, sample_weight=weights_train, epochs=i, num_threads=2)
        record.append(time.time() - start_time)
        record.append(precision_at_k(model, interactions_train, k=10).mean())
        record.append(precision_at_k(model, interactions_test, k=10).mean())
        print(precision_at_k(model, interactions_test, k=10).mean())
        record.append(recall_at_k(model, interactions_train, k=10).mean())
        record.append(recall_at_k(model, interactions_test, k=10).mean())

        records.append(record)

    # df = pd.DataFrame(records, columns=['Epoch', 'Exe Time', 'Precision@10 (Train)', 'Precision@10 (Test)', 'Recall@10 (Train)', 'Recall@10 (Test)'])
    # df.to_csv('traing/data.csv', header=True)


class Command(BaseCommand):
    help = "Train model"

    def handle(self, *args, **options):
        new_train()
