from celery import Celery
from celery.five import monotonic
from celery.utils.log import get_task_logger
from contextlib import contextmanager
from django.core.cache import cache
from django.utils import timezone
from book.management.commands.train import DataPrep, DataFit, RecModel
import pickle
from book.models import MachineLearning

logger = get_task_logger(__name__)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('tasks')

LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes

@contextmanager
def memcache_lock():
    timeout_at = monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    status = cache.add('lock', 'lock', LOCK_EXPIRE)
    try:
        yield status
    finally:
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if monotonic() < timeout_at and status:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)

@app.task(bind=True)
def train_model_new_user(self, feed_url):
    saved_obj = MachineLearning.objects.first().value
    dataFit = saved_obj["data"]
    recModel = saved_obj["model"]
    
    interactions, weights = dataFit.fit()
    new_checkpoint = timezone.now()

    recModel.fit(interactions, weights)
    recModel.set_checkpoint(new_checkpoint)
    to_be_saved = {
        "data": dataFit,
        "model": recModel
    }

    with memcache_lock() as acquired:
        if not acquired:
            self.retry()
        else:
            ml_obj.value = to_be_saved
            ml_obj.save()       
    
@app.task(bind=True)
def train_model_new_rating(self, feed_url):
    ml_obj = MachineLearning.objects.first()
    saved_obj = ml_obj.value
    dataFit = saved_obj["data"]
    recModel = saved_obj["model"]

    interactions, weights = dataFit.create_new_interactions(recModel.checkpoint)
    new_checkpoint = timezone.now()
    recModel.fit_partial(interactions, weights)
    recModel.set_checkpoint(new_checkpoint)
    to_be_saved = {
        "data": dataFit,
        "model": recModel
    }
    with memcache_lock() as acquired:
        if not acquired:
            self.retry()
        else:
            ml_obj.value = to_be_saved
            ml_obj.save()
