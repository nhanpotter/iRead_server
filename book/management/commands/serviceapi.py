import requests, random
from lxml import html
from django.core.management.base import BaseCommand, CommandError
from book.models import Book, Genre

DATA_API = 'https://data.gov.sg/api/action/datastore_search?resource_id=835e630b-a03f-4f77-baa6-9c69c91883f2'

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True

def web_scraping(resource_url):
    """
    Get downloadable URL for the book
    """
    filtered_data = {}
    page = requests.get(resource_url)
    tree = html.fromstring(page.text)
    download = tree.xpath('//a[@title="Download now"]/@href')
    download_url = 'https:' + download[0]
    if is_downloadable(download_url):
        print("Success")
        filtered_data['resource_url'] = download_url
    else:
        print("Fail")
        filtered_data['resource_url'] = ""

    title = tree.xpath('//body/div[2]/div[3]/div[2]/div[1]/h3/a/@title')[0]
    filtered_data['book_title'] = title

    summary = tree.xpath('//p[@class="detail-description"]/text()')[0]
    filtered_data['summary'] = summary
    return filtered_data

def refine_book_data(record):
    """
    Refine all data necessary for the book
    """
    resource_url = record['resource_url']
    filtered_data = web_scraping(resource_url)
    record['book_title'] = filtered_data['book_title']
    record['summary'] = filtered_data['summary']
    record['resource_url'] = filtered_data['resource_url']
    record['item_format'] = record.pop('format')
    record['item_copyright'] = record.pop('copyright')
    record['id'] = record.pop('_id')

    # Genre
    genre_list = Genre.objects.all()
    record['genre'] = random.choice(genre_list)

    return record
    


def get_book_data():
    """
    Get raw book data from api
    """
    get_request = requests.get(DATA_API)
    get_data = get_request.json()
    if not get_data['success']:
        print("Fail to get api data")
        return

    records = get_data['result']['records']
    for record in records:
        record = refine_book_data(record)
        try:
            Book.objects.create(**record)
        except:
            print("This book is already created")


class Command(BaseCommand):
    help = 'Get book data from API'

    def handle(self, *args, **options):
        get_book_data()